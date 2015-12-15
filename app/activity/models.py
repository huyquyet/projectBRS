# Create your models here.

from django.db import models
from django.utils import timezone
from mongoengine import IntField, EmbeddedDocument, DateTimeField, StringField, BooleanField, EmbeddedDocumentListField, \
    ListField, EmbeddedDocumentField

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
    _id = IntField()
    date_time = DateTimeField(None)
    type_activity = IntField()
    object_id = IntField()
    data = StringField()
    status = BooleanField(default=True)

    class Meta:
        app_label = 'no_sql'


class DictKey(EmbeddedDocument):
    date_time = DateTimeField(timezone.now)


class Activities(Document):
    _id = IntField()
    action = EmbeddedDocumentListField(Activity)
    # action = ListField(EmbeddedDocumentField(Activity))
    # action = DictField()

    class Meta:
        app_label = 'no_sql'
