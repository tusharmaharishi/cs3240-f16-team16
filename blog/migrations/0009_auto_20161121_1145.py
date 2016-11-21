# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='folder',
            field=models.ForeignKey(default=0, blank=True, to='blog.Folder', null=True),
        ),
    ]
