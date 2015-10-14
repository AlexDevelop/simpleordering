# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20151002_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 14, 16, 7, 15, 46827), verbose_name='Order / Delivery date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(default='Inventory naar Klant', max_length=255, choices=[(b'0', 'Inventory naar Klant'), (b'1', 'Klant naar Inventory'), (b'2', 'Guidion naar Inventory'), (b'3', 'Inventory naar Guidion')]),
        ),
    ]
