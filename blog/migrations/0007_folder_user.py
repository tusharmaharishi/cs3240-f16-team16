# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20161120_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='user',
            field=models.CharField(max_length=100, default=0),
            preserve_default=False,
        ),
    ]
