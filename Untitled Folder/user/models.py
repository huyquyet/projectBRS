from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from projectBRS import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    avata = models.ImageField(upload_to=settings.AVATA_DIR, max_length=255, default='', blank=False)

    follows = models.ManyToManyField('self', through='Follow', through_fields=('followee', 'follower'),
                                     related_name='following', symmetrical=False)

class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follower')
    followee = models.ForeignKey(UserProfile, related_name='followee')
