from django.urls import path
from . import views

urlpatterns = [
    path("", views.desktop_view, name="desktop"),
    path('explorer/', views.list_directory, name='list_directory'),
    path('file/',views.file, name='file')
]