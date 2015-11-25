# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0008_savedpostvisibilities_savedpostvisibilitiesattributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedpostvisibilities',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
