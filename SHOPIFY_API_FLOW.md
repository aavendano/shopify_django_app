# Flujo de la API de Shopify en este proyecto

Este documento describe, en espanol, como funciona la integracion con Shopify dentro de este repositorio. El objetivo es que puedas entender rapidamente el flujo sin tener que reconstruirlo leyendo todos los archivos del proyecto.

## Resumen

Este proyecto es un ejemplo de aplicacion Django que:

1. pide la URL de una tienda Shopify,
2. inicia el flujo OAuth con Shopify,
3. recibe el callback de autorizacion,
4. valida la respuesta,
5. obtiene un `access_token`,
6. guarda ese token en la sesion de Django,
7. activa la sesion de Shopify en cada request autenticado,
8. hace llamadas a la API usando la libreria `ShopifyAPI`.

## Archivos principales

- `shopify_app/views.py`
  Contiene el flujo de login, redireccion a Shopify y finalizacion del OAuth.
- `shopify_app/middleware.py`
  Activa la sesion autenticada de Shopify en cada request.
- `shopify_app/decorators.py`
  Protege vistas que requieren haber iniciado sesion con una tienda.
- `shopify_app/apps.py`
  Lee la configuracion de entorno: API key, secret, version y scopes.
- `home/views.py`
  Muestra ejemplos simples de llamadas a la API de Shopify.

## Variables de entorno

La configuracion se toma desde variables de entorno definidas en `shopify_app/apps.py`:

- `SHOPIFY_API_KEY`
  API key de la app creada en Shopify.
- `SHOPIFY_API_SECRET`
  Secret de la app.
- `SHOPIFY_API_VERSION`
  Version de la API a usar. Si no existe, este proyecto usa `unstable`.
- `SHOPIFY_API_SCOPE`
  Lista de permisos separados por comas. Por defecto:
  `read_products,read_orders`
- `DJANGO_SECRET`
  Secret key de Django.

## Flujo completo

### 1. El usuario entra a la app

La aplicacion corre en Django y expone rutas bajo `/shopify/`.

Las rutas principales son:

- `/shopify/login/`
- `/shopify/authenticate/`
- `/shopify/finalize/`
- `/shopify/logout/`

Estas rutas estan definidas en `shopify_app/urls.py`.

### 2. El usuario indica la tienda

La vista `login()` en `shopify_app/views.py` muestra un formulario donde el usuario ingresa la tienda, por ejemplo:

`mi-tienda.myshopify.com`

Si la URL ya trae el parametro `shop`, la vista salta directamente a `authenticate()`.

## 3. Se inicia OAuth con Shopify

La vista `authenticate()` hace lo siguiente:

1. lee el `shop` desde `GET` o `POST`,
2. valida que exista,
3. obtiene los scopes configurados,
4. construye la URL de callback usando `reverse(finalize)`,
5. genera un valor aleatorio `state`,
6. guarda ese `state` en la sesion de Django,
7. crea la URL de permisos de Shopify,
8. redirige al usuario a Shopify para autorizar la app.

La llamada clave es:

```python
permission_url = _new_session(shop_url).create_permission_url(scope, redirect_uri, state)
```

Ese paso delega a Shopify la pantalla de autorizacion.

## 4. Shopify redirige al callback

Despues de autorizar, Shopify redirige al usuario a `/shopify/finalize/` con parametros en la query string, incluyendo:

- `shop`
- `state`
- `hmac`
- `code`

La vista `finalize()` procesa esa respuesta.

## 5. Se valida el parametro `state`

Primero se compara el `state` recibido con el `state` guardado previamente en la sesion:

- si no coincide, el login se rechaza,
- si coincide, se elimina de la sesion.

Esto protege contra ataques de falsificacion de solicitudes.

## 6. Se valida el `hmac`

Despues, la vista toma todos los parametros del callback, separa el `hmac`, ordena el resto y reconstruye la cadena firmada.

Luego calcula un HMAC SHA-256 usando `SHOPIFY_API_SECRET` y compara el resultado con el `hmac` enviado por Shopify.

Si no coincide:

- se muestra un error,
- el login se cancela.

Esto permite verificar que la respuesta realmente fue generada por Shopify y no fue manipulada.

## 7. Se solicita el `access_token`

Si las validaciones pasan, el proyecto crea una sesion Shopify para esa tienda y ejecuta:

```python
session.request_token(request.GET)
```

Con eso intercambia el `code` del callback por un `access_token`.

## 8. El token se guarda en la sesion de Django

Cuando Shopify devuelve el token, el proyecto guarda estos datos en `request.session['shopify']`:

```python
{
    "shop_url": shop_url,
    "access_token": access_token
}
```

Eso significa que la autenticacion queda asociada a la sesion web actual del usuario.

## 9. El middleware activa la sesion Shopify en cada request

`shopify_app/middleware.py` contiene `LoginProtection`, que hace dos tareas importantes.

### Configuracion inicial

En `__init__()`:

- lee `SHOPIFY_API_KEY` y `SHOPIFY_API_SECRET`,
- valida que existan,
- ejecuta `shopify.Session.setup(...)`.

Esa configuracion inicial prepara la libreria `ShopifyAPI`.

### Activacion por request

En `__call__()`:

1. revisa si existe `request.session['shopify']`,
2. crea una `shopify.Session` usando `shop_url` y `SHOPIFY_API_VERSION`,
3. asigna el `access_token`,
4. activa la sesion con:

```python
shopify.ShopifyResource.activate_session(shopify_session)
```

Despues de ejecutar la vista, limpia la sesion activa con:

```python
shopify.ShopifyResource.clear_session()
```

Esto evita que la sesion autenticada quede contaminando otros requests.

## 10. Las vistas protegidas ya pueden usar la API

El decorador `shop_login_required` en `shopify_app/decorators.py` verifica que exista una sesion Shopify dentro de `request.session`.

Si no existe:

- guarda la URL actual en `return_to`,
- redirige al login.

Si existe, deja pasar la request.

Gracias a esto, en `home/views.py` se pueden hacer llamadas como:

```python
products = shopify.Product.find(limit=3)
orders = shopify.Order.find(limit=3, order="created_at DESC")
```

Estas llamadas funcionan porque el middleware ya activo la sesion de Shopify antes de entrar a la vista.

## Flujo resumido en una sola secuencia

1. Usuario abre la app.
2. Ingresa su tienda Shopify.
3. Django genera `state` y redirige a Shopify.
4. Shopify muestra autorizacion.
5. Shopify redirige a `/shopify/finalize/`.
6. Django valida `state`.
7. Django valida `hmac`.
8. Django intercambia `code` por `access_token`.
9. Django guarda `shop_url` y `access_token` en la sesion.
10. En requests posteriores, el middleware activa la sesion Shopify.
11. Las vistas llaman a la API usando `shopify.Product`, `shopify.Order`, etc.

## Consideraciones importantes

### Este ejemplo usa un enfoque clasico

El proyecto usa:

- Django con sesiones del lado del servidor,
- la libreria `ShopifyAPI`,
- un flujo OAuth clasico,
- llamadas basadas en recursos como `shopify.Product.find(...)`.

Es un enfoque util para aprender el flujo base, pero no representa necesariamente la arquitectura mas moderna de apps embebidas de Shopify.

### La version por defecto es `unstable`

En este proyecto, si no defines `SHOPIFY_API_VERSION`, se usa `unstable`.

Para trabajo real, normalmente conviene fijar una version explicita de la API para evitar cambios inesperados.

### Los scopes controlan el acceso

Si una vista quiere consultar pedidos, productos u otros recursos, la app necesita los permisos correctos en `SHOPIFY_API_SCOPE`.

Por ejemplo:

- `read_products`
- `read_orders`

Sin esos scopes, Shopify puede rechazar las llamadas aunque el login haya sido exitoso.

## Ejemplo mental rapido

Piensalo asi:

- `views.py` consigue el permiso,
- `finalize()` consigue el token,
- la sesion de Django guarda ese token,
- el middleware convierte ese token en una sesion activa de Shopify,
- las vistas del negocio consumen la API ya autenticadas.

## Punto de partida para extender la app

Si quieres agregar mas integracion con Shopify, normalmente lo haras en vistas o servicios nuevos que usen la sesion ya activada por el middleware.

Ejemplos:

- listar mas productos,
- crear webhooks,
- consultar clientes,
- actualizar inventario,
- leer metafields.

Antes de eso, revisa siempre:

1. que la ruta este protegida,
2. que el token exista en la sesion,
3. que el scope necesario este configurado,
4. que la version de API sea la correcta.
