from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from mongoengine import IntField, StringField, ListField, ImageField, EmbeddedDocumentField

from app.friend.models import Friend, Waiting, Block, Request
from django_mongoengine.utils.module import Document
from projectBRS import settings


# Create your models here.

def _path_to_avatar(instance, filename):
    return '{user_id}/{dir_name}/{file_name}'.format(user_id=instance.user.id, dir_name=settings.AVATAR_DIR,
                                                     file_name=filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    avatar = models.ImageField(upload_to=_path_to_avatar, max_length=255, default='avatar/default.jpg', blank=False)

    follows = models.ManyToManyField('self', through='Follow', through_fields=('followee', 'follower'),
                                     related_name='following', symmetrical=False)
    status = models.BooleanField(default=True)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follower')  # Nguoi theo doi
    followee = models.ForeignKey(UserProfile, related_name='followee')  # Nguoi dc theo doi
    date = models.DateTimeField(default=timezone.now)


class Profile(Document):
    _id = IntField()
    avatar = ImageField(collection_name='images', size=(6000, 4000, True), thumbnail_size=(400, 400, True),
                        default=None)
    full_name = StringField(max_length=255)
    other_name = StringField(max_length=255)
    friend = ListField(EmbeddedDocumentField(Friend))
    waiting = ListField(EmbeddedDocumentField(Waiting))
    request = ListField(EmbeddedDocumentField(Request))
    block = ListField(EmbeddedDocumentField(Block))

    def __unicode__(self):
        return self._id

    class Meta:
        app_label = 'no_sql'
