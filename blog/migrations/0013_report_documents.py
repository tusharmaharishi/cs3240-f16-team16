# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20161201_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='documents',
            field=models.ManyToManyField(to='blog.Document'),
        ),
    ]
