# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20150715_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(default='test', max_length=255, verbose_name='code'),
            preserve_default=False,
        ),
    ]
