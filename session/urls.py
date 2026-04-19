from django.urls import path

from .views import SessionDetailView

app_name = "session"

urlpatterns = [
    path("<str:pk>/", SessionDetailView.as_view(), name="detail"),
]
