# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        ('comment', '0001_initial'),
        ('user', '0002_auto_20151020_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentreview',
            name='review',
            field=models.ForeignKey(related_name='comment', to='review.Review'),
        ),
        migrations.AddField(
            model_name='commentreview',
            name='user_profile',
            field=models.ForeignKey(related_name='comment_review', to='user.UserProfile'),
        ),
    ]
