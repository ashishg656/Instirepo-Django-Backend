# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsonposts',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
