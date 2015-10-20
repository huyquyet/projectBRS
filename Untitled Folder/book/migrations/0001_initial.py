# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('slug', models.SlugField(max_length=500)),
                ('title', models.TextField()),
                ('cover', models.ImageField(upload_to='books', default='', max_length=255)),
                ('description', models.TextField(blank=True, default='')),
                ('author', models.TextField()),
                ('publish', models.TextField()),
                ('page', models.IntegerField()),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(related_name='book', to='category.Category')),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('book', models.ForeignKey(related_name='favorite', to='book.Book')),
                ('user', models.ForeignKey(related_name='favorite', to='user.UserProfile')),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('rate', models.IntegerField(default=0)),
                ('book', models.ForeignKey(related_name='rating', to='book.Book')),
                ('user', models.ForeignKey(related_name='rating', to='user.UserProfile')),
            ],
            options={
                'db_table': 'rating',
            },
        ),
        migrations.CreateModel(
            name='ReadReading',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.IntegerField()),
                ('book', models.ForeignKey(related_name='read_reading', to='book.Book')),
                ('user', models.ForeignKey(related_name='read_reading', to='user.UserProfile')),
            ],
            options={
                'db_table': 'read_reading',
            },
        ),
    ]
