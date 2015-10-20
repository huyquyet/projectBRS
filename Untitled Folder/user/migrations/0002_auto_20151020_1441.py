# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('followee', models.ForeignKey(related_name='followee', to='user.UserProfile')),
                ('follower', models.ForeignKey(related_name='follower', to='user.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follows',
            field=models.ManyToManyField(related_name='following', through='user.Follow', to='user.UserProfile'),
        ),
    ]
