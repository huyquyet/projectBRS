# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sendbybook', '0003_auto_20151027_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='bybook',
            name='del_status',
            field=models.BooleanField(default=True),
        ),
    ]
