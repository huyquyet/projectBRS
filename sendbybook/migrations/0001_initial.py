# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ByBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField()),
                ('author', models.TextField()),
                ('publish', models.TextField()),
                ('page', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('user_profile', models.ForeignKey(to='user.UserProfile', related_name='by_book')),
            ],
            options={
                'db_table': 'bybook',
            },
        ),
    ]
