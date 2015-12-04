# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0009_savedpostvisibilities_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('read', models.BooleanField(default=False)),
                ('sent_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sent_by')),
                ('sent_from', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sent_from')),
            ],
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='last_message_read_timestamp',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
