# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20151027_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avata',
            field=models.ImageField(upload_to='avata', default='avata/default.jpg', max_length=255),
        ),
    ]
