# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_follow_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='date_level',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
