# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20161121_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='folder',
            field=models.ForeignKey(default=None, blank=True, null=True, to='blog.Folder'),
        ),
    ]
