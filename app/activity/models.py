# Create your models here.
from django.db import models
from django.utils import timezone
from mongoengine import IntField, ListField, EmbeddedDocument, DateTimeField, StringField, EmbeddedDocumentField

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


# class Activity(object):
#     def __init__(self, time, date, type, data=None):
#         self._time = time
#         self._date = date
#         self._type = type
#         self._data = data
#
#     # get set property
#     @property
#     def time(self):
#         return self._time
#
#     @time.setter
#     def time(self, value):
#         self._time = value
#
#     @property
#     def date(self):
#         return self._date
#
#     @date.setter
#     def date(self, value):
#         self._date = value
#
#     @property
#     def type(self):
#         return self._type
#
#     @type.setter
#     def type(self, value):
#         self._type = value
#
#     @property
#     def data(self):
#         return self._data
#
#     @data.setter
#     def data(self, value):
#         self._data = value

class Activity(EmbeddedDocument):
    time = DateTimeField(default=timezone.now)
    type_activity = IntField()
    data = StringField()

    class Meta:
        app_label = 'no_sql'


class Activities(Document):
    _id = IntField()
    activity = ListField(EmbeddedDocumentField(Activity))

    class Meta:
        app_label = 'no_sql'
