from django.urls import path

from . import views


app_name = "core"

urlpatterns = [
    path("", views.PublicEntryView.as_view(), name="public-entry"),
    path("auth/login", views.AuthLoginView.as_view(), name="auth-login"),
    path("auth/patch-id-token", views.AuthPatchIdTokenView.as_view(), name="auth-patch-id-token"),
    path(
        "auth/embedded/redirect",
        views.EmbeddedInAppRedirectView.as_view(),
        name="auth-embedded-redirect",
    ),
    path(
        "auth/embedded/parent-redirect",
        views.EmbeddedParentRedirectView.as_view(),
        name="auth-embedded-parent-redirect",
    ),
    path("app/", views.HomeView.as_view(), name="home"),
]
