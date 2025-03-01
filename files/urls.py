from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_view, name='file_view'),  
    path('upload/', views.upload_file, name='upload_file'),  
]
