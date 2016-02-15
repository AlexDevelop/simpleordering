# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20150715_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(related_name='customer', blank=True, to='order.Customer', null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='housenumber_addition',
            field=models.CharField(default=None, max_length=10, null=True, verbose_name='housenumber addition', blank=True),
        ),
    ]
