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
    status = models.IntegerField(default=0)

    """
    status
    0 : Waiting
    1 : Successful
    2 : Fail
    """

    class Meta:
        db_table = 'bybook'
