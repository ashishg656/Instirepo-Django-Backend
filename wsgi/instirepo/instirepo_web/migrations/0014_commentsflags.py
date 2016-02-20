# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0013_usersblocklist'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsFlags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(to='instirepo_web.CommentsOnPosts')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
