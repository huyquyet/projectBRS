# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20151207_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='level',
            field=models.IntegerField(default=5),
        ),
    ]
