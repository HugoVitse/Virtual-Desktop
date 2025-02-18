from django.db import models


class File(models.Model):
    filename = models.CharField(max_length=20)
    filesize = models.IntegerField()

