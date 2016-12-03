# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20161203_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='long_description',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
