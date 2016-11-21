# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='document',
            field=models.FileField(default=datetime.datetime(2016, 11, 21, 2, 47, 22, 186404, tzinfo=utc), upload_to='documents/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
