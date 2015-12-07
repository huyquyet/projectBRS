from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from projectBRS import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    avata = models.ImageField(upload_to=settings.AVATA_DIR, max_length=255, default='avata/default.jpg', blank=False)

    follows = models.ManyToManyField('self', through='Follow', through_fields=('followee', 'follower'),
                                     related_name='following', symmetrical=False)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follower')  # Nguoi theo doi
    followee = models.ForeignKey(UserProfile, related_name='followee')  # Nguoi dc theo doi
    date = models.DateTimeField(default=timezone.now)