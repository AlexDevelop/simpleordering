# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20150715_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name='Order / Delivery date'),
        ),
    ]
