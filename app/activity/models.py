# Create your models here.

from django.db import models
from django.utils import timezone
from mongoengine import IntField, ListField, EmbeddedDocument, DateTimeField, StringField, EmbeddedDocumentField, \
    BooleanField

from django_mongoengine.utils.module import Document

"""
Data TypeActivity
1:rating_book
2:read_book
3:finish_book
4:write_review
5:write_comment
6:like_review
7:like_comment
8:follow_user
9:unfollow_user
10:friend_user
11:unfriend_user
12:send_book
"""


class TypeActivity(models.Model):
    name = models.CharField(max_length=255)


class Activity(EmbeddedDocument):
    # time = DateTimeField(default=None)
    # date = DateTimeField(default=None)
    date_time = DateTimeField(default=timezone.now)
    type_activity = IntField()
    object_id = IntField()
    data = StringField()
    status = BooleanField(default=True)

    class Meta:
        app_label = 'no_sql'


class Activities(Document):
    _id = IntField()
    action = ListField(EmbeddedDocumentField(Activity))

    class Meta:
        app_label = 'no_sql'
