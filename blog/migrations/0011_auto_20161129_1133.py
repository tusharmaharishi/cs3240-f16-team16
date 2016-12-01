# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0010_auto_20161121_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('private', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=255, blank=True)),
                ('document', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('upload_at', models.DateTimeField(auto_now_add=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(blank=True, null=True, default=None, to='blog.Folder')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='folder',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
