# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_userprofile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=app.user.models._path_to_avatar, max_length=255, default='avatar/default.jpg'),
        ),
    ]
