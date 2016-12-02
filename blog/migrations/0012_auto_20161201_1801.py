# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20161129_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/%Y/%m/%d')),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='document',
        ),
    ]
