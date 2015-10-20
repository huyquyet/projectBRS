# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20151020_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='ByBook',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.TextField()),
                ('author', models.TextField()),
                ('publish', models.TextField()),
                ('page', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('user_profile', models.ForeignKey(related_name='by_book', to='user.UserProfile')),
            ],
            options={
                'db_table': 'bybook',
            },
        ),
    ]
