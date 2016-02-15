# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20150710_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default=None, max_length=2048, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Order Quantity'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Order Quantity'),
        ),
    ]
