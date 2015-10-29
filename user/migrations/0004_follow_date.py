# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20151027_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
