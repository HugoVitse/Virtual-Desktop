from django.db import models
import os

from users.models import CustomUser

FILE_TYPE_CHOICES = [
    ('txt', 'Texte'),
    ('image', 'Image'),
]

def user_directory_path(instance, filename):
    """
    Retourne le chemin de destination du fichier.
    Si instance.name contient un chemin (ex: '/Pictures/image.jpg'),
    il sera utilisé (après avoir retiré le slash initial) ;
    sinon, on utilisera le nom original du fichier.
    """
    # Utilise la valeur du champ name si elle est renseignée, sinon filename
    custom_path = instance.name or filename
    print(custom_path)
    # Retire le slash initial s'il y en a un pour éviter un chemin absolu
    custom_path = custom_path.lstrip('/')
    return os.path.join('files', str(instance.user.id), custom_path)

class File(models.Model):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=FILE_TYPE_CHOICES, default='txt')
    file_path = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return self.name

    def save(self,path, *args, **kwargs):
        # Si le champ file est renseigné, on enregistre son chemin dans file_path
        print(f'{path}/{self.file.name}')
        if self.file:
            self.name = f'{path}/{self.file.name}'
            self.file_path = f'{path}/{self.file.name}'

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return os.path.join('files', self.file_path)
