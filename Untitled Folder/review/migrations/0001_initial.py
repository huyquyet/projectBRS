# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('user', '0002_auto_20151020_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeReview',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(related_name='review', to='book.Book')),
                ('like', models.ManyToManyField(related_name='like_review', through='review.LikeReview', to='user.UserProfile')),
                ('user_profile', models.ForeignKey(related_name='review', to='user.UserProfile')),
            ],
            options={
                'db_table': 'review',
            },
        ),
        migrations.AddField(
            model_name='likereview',
            name='review',
            field=models.ForeignKey(related_name='likereview', to='review.Review'),
        ),
        migrations.AddField(
            model_name='likereview',
            name='user_profile',
            field=models.ForeignKey(related_name='likereview', to='user.UserProfile'),
        ),
    ]
