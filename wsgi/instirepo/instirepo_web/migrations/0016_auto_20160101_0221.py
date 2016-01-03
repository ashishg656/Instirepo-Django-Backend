# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0015_auto_20151231_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='web_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postvisibility',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
