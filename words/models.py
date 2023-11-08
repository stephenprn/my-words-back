from django.db import models

# Create your models here.

class WordDefinition(models.Model):
    word = models.CharField(max_length=255)
    definition = models.TextField()
    note = models.TextField()
    slug = models.CharField(max_length=255)
