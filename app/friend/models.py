# Create your models here.
from django.utils import timezone
from mongoengine.fields import EmbeddedDocument, IntField, DateTimeField, BooleanField


class Friend(EmbeddedDocument):
    user = IntField()
    create = DateTimeField(default=timezone.now)
    destroy = DateTimeField(default=None)
    status = BooleanField(default=False)

    class Mete:
        app_label = 'no_sql'


class Waiting(EmbeddedDocument):
    user = IntField
    date = DateTimeField(default=timezone.now)

    class Mete:
        app_label = 'no_sql'


class Request(EmbeddedDocument):
    user = IntField()
    date = DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'no_sql'


class Block(EmbeddedDocument):
    user = IntField()
    date = DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'no_sql'
