from django.urls import path
from . import views
from .views import desktop_view

urlpatterns = [
    path("", views.desktop_view, name="desktop"),
    path('explorer/', views.list_directory, name='list_directory'),
    path('file/',views.file, name='file'),
    path("terminal/", desktop_view, name="terminal")
]