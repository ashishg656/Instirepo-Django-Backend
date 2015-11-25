# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instirepo_web', '0007_postcategories_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedPostVisibilities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedPostVisibilitiesAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(max_length=255, choices=[('branch', 'Branch'), ('year', 'Year'), ('batch', 'Batch'), ('teacher', 'Teacher')])),
                ('batch', models.ForeignKey(to='instirepo_web.Batches', null=True, blank=True)),
                ('branch', models.ForeignKey(to='instirepo_web.Branches', null=True, blank=True)),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('visibility', models.ForeignKey(to='instirepo_web.SavedPostVisibilities')),
                ('year', models.ForeignKey(to='instirepo_web.StudentYears', null=True, blank=True)),
            ],
        ),
    ]
