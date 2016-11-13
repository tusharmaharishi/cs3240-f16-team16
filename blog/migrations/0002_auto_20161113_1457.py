# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usergroup',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, serialize=False, parent_link=True, to='auth.Group', primary_key=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=('auth.group',),
        ),
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='document',
            field=models.FileField(upload_to='documents/', default=datetime.datetime(2016, 11, 13, 19, 57, 15, 236778, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='upload_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 11, 13, 19, 57, 35, 901693, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
