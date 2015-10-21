from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.TextField(max_length=255)
