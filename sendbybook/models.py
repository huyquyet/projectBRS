from django.db import models

# Create your models here.
from user.models import UserProfile


class ByBook(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='by_book')
    name = models.TextField()
    author = models.TextField()
    publish = models.TextField()
    page = models.IntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table = 'bybook'
