# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sendbybook', '0002_bybook_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bybook',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
