from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file_type', 'file']  # on ne passe pas file_path car il est généré automatiquement
