# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(to='book.Book', related_name='review_book')),
                ('like', models.ManyToManyField(related_name='like_review', through='review.LikeReview', to='user.UserProfile')),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='review_user')),
            ],
            options={
                'db_table': 'review',
            },
        ),
        migrations.AddField(
            model_name='likereview',
            name='review',
            field=models.ForeignKey(to='review.Review', related_name='like_review'),
        ),
        migrations.AddField(
            model_name='likereview',
            name='user_profile',
            field=models.ForeignKey(to='user.UserProfile', related_name='like_review_user'),
        ),
    ]
