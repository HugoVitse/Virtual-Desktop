from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_view, name='file_view'),  # Vue de l'explorateur de fichiers
    path('upload/', views.upload_file, name='upload_file'),  # Vue pour télécharger un fichier
]
