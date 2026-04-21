
from django.contrib import admin
from django.urls import path, include
from core.views import HomeView

urlpatterns = [
    path("core/", include("core.urls")),
    path("webhooks/", include("webhooks.urls")),
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
]
