# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('batch_name', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Branches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('branch_name', models.TextField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CommentsOnPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('comment', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FlaggedPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PollChoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('choice', models.TextField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PollsVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('choice', models.ForeignKey(to='instirepo_web.PollChoices')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts_categories_images')),
                ('is_public', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('event', 'Event'), ('placement', 'Placement'), ('poll', 'Poll'), ('other', 'Other')], default='other', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('heading', models.TextField(null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts_images')),
                ('company_name', models.TextField(blank=True, null=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('is_public', models.BooleanField(default=False)),
                ('is_by_teacher', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='instirepo_web.PostCategories')),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostVisibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(null=True, blank=True, to='instirepo_web.Batches')),
                ('branch', models.ForeignKey(null=True, blank=True, to='instirepo_web.Branches')),
                ('college', models.ForeignKey(null=True, blank=True, to='instirepo_web.College')),
                ('individual', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(to='instirepo_web.Posts')),
            ],
        ),
        migrations.CreateModel(
            name='SavedPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='instirepo_web.Posts')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentYears',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('year_name', models.TextField(max_length=255)),
                ('admission_year', models.IntegerField()),
                ('passout_year', models.IntegerField()),
                ('has_passed_out', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(to='instirepo_web.Branches')),
            ],
        ),
        migrations.CreateModel(
            name='Universities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UpvotesOnPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('is_upvote', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='instirepo_web.Posts')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('userIDAuth', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(blank=True, null=True, max_length=20)),
                ('access_token', models.TextField(blank=True, null=True)),
                ('refresh_token', models.TextField(blank=True, null=True)),
                ('profile_details_json_object', models.TextField(blank=True, null=True)),
                ('profile_image', models.TextField(blank=True, null=True)),
                ('device_id', models.TextField(blank=True, null=True, max_length=200)),
                ('is_student_coordinator', models.BooleanField(default=False)),
                ('is_professor', models.BooleanField(default=False)),
                ('is_senior_professor', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('enrollment_number', models.CharField(blank=True, null=True, max_length=255)),
                ('has_provided_college_details', models.BooleanField(default=False)),
                ('is_email_shown_to_others', models.BooleanField(default=False)),
                ('is_mobile_shown_to_others', models.BooleanField(default=False)),
                ('resume', models.TextField(blank=True, null=True)),
                ('batch', models.ForeignKey(null=True, blank=True, to='instirepo_web.Batches')),
                ('branch', models.ForeignKey(null=True, blank=True, to='instirepo_web.Branches')),
                ('college', models.ForeignKey(null=True, to='instirepo_web.College')),
                ('university', models.ForeignKey(null=True, blank=True, to='instirepo_web.Universities')),
                ('user_obj', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_profile')),
                ('year', models.ForeignKey(null=True, blank=True, to='instirepo_web.StudentYears')),
            ],
        ),
        migrations.AddField(
            model_name='postvisibility',
            name='university',
            field=models.ForeignKey(null=True, blank=True, to='instirepo_web.Universities'),
        ),
        migrations.AddField(
            model_name='postvisibility',
            name='year',
            field=models.ForeignKey(null=True, blank=True, to='instirepo_web.StudentYears'),
        ),
        migrations.AddField(
            model_name='pollsvotes',
            name='post',
            field=models.ForeignKey(to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='pollsvotes',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pollchoices',
            name='post',
            field=models.ForeignKey(to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='flaggedposts',
            name='post',
            field=models.ForeignKey(to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='flaggedposts',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentsonposts',
            name='post',
            field=models.ForeignKey(to='instirepo_web.Posts'),
        ),
        migrations.AddField(
            model_name='commentsonposts',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='college',
            name='university',
            field=models.ForeignKey(to='instirepo_web.Universities'),
        ),
        migrations.AddField(
            model_name='branches',
            name='college',
            field=models.ForeignKey(to='instirepo_web.College'),
        ),
        migrations.AddField(
            model_name='batches',
            name='year',
            field=models.ForeignKey(to='instirepo_web.StudentYears'),
        ),
    ]
