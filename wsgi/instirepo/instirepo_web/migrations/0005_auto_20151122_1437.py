# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0004_postcategories_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpvotesOnUsers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('is_upvote', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('upvoter', models.ForeignKey(related_name='user_who_voted', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user_being_voted', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='designation',
            field=models.CharField(default='Student', max_length=255, null=True),
        ),
    ]
