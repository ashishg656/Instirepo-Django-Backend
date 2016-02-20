# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instirepo_web', '0011_auto_20151202_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='message',
            field=models.TextField(null=True),
        ),
    ]
