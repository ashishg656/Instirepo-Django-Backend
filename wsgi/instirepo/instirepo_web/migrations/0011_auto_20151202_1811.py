# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0010_auto_20151202_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='sent_by',
        ),
        migrations.RemoveField(
            model_name='messages',
            name='sent_from',
        ),
        migrations.AddField(
            model_name='messages',
            name='receiver',
            field=models.ForeignKey(related_name='receiver', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='messages',
            name='sender',
            field=models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
