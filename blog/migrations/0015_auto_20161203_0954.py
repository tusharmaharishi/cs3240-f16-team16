# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_report_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='description',
            new_name='long_description',
        ),
        migrations.AddField(
            model_name='report',
            name='short_description',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='group',
            field=models.CharField(max_length=100, blank=True, default=''),
        ),
    ]
