from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.TextField(max_length=255)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name
