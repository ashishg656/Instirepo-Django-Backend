# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0005_auto_20151122_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofiles',
            name='has_reached_post_limit',
            field=models.BooleanField(default=False),
        ),
    ]
