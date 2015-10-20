# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20151020_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReview',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'comment_review',
            },
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.ForeignKey(related_name='like_comment', to='comment.CommentReview')),
                ('user_profile', models.ForeignKey(related_name='like_comment', to='user.UserProfile')),
            ],
        ),
    ]
