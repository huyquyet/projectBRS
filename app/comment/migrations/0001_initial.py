# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('review', models.ForeignKey(to='review.Review', related_name='comment')),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='comment_review')),
            ],
            options={
                'db_table': 'comment_review',
            },
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.ForeignKey(to='comment.CommentReview', related_name='like_comment')),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='like_comment_user')),
            ],
        ),
    ]
