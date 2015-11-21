# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0003_postseens'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcategories',
            name='color',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
