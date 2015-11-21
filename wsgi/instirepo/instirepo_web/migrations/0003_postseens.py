# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0002_commentsonposts_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostSeens',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='instirepo_web.Posts')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
