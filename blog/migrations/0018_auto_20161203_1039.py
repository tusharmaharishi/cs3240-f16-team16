# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20161203_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
