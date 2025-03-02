from django.db import models


class File(models.Model):
    filename = models.CharField(max_length=20)
    filesize = models.IntegerField()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)