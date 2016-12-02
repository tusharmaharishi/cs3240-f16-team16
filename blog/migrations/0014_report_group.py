# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_report_documents'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='group',
            field=models.CharField(max_length=100, default=''),
        ),
    ]
