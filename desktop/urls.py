from django.urls import path
from . import views
from .views import desktop_view

urlpatterns = [
    path("", views.desktop_view, name="desktop"),
    path("terminal/", desktop_view, name="terminal")
]