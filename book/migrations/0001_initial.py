# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(max_length=500)),
                ('title', models.TextField()),
                ('cover', models.ImageField(default='', upload_to='books', max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('author', models.TextField()),
                ('publish', models.TextField()),
                ('page', models.IntegerField()),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(to='category.Category', related_name='book')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(to='book.Book', related_name='favorite_book')),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='favorite_user')),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('rate', models.IntegerField(default=0)),
                ('book', models.ForeignKey(to='book.Book', related_name='rating_book')),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='rating_user')),
            ],
            options={
                'db_table': 'rating',
            },
        ),
        migrations.CreateModel(
            name='ReadReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField()),
                ('book', models.ForeignKey(to='book.Book', related_name='read_reading_book')),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='read_reading_user')),
            ],
            options={
                'db_table': 'read_reading',
            },
        ),
    ]
