# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0006_userprofiles_has_reached_post_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcategories',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
