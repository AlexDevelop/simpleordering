# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20150715_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(default='Inventory naar Klant', max_length=255, choices=[(0, 'Inventory naar Klant'), (1, 'Klant naar Inventory'), (2, 'Guidion naar Inventory'), (3, 'Inventory naar Guidion')]),
        ),
    ]
