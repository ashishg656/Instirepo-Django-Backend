# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0012_messages_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersBlockList',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('comment', models.TextField(null=True, blank=True)),
                ('blocked_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='blocked_by')),
                ('blocked_user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='blocked_user')),
            ],
        ),
    ]
