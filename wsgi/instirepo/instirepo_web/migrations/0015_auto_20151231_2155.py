# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0014_commentsflags'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowingPosts',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='notifications_images')),
                ('image_url', models.TextField(blank=True, null=True)),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofiles',
            name='last_notification_seen_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='uploader',
            field=models.ForeignKey(related_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postvisibility',
            name='post',
            field=models.ForeignKey(related_name='post', to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='post',
            field=models.ForeignKey(blank=True, null=True, to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='followingposts',
            name='post',
            field=models.ForeignKey(to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='followingposts',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
