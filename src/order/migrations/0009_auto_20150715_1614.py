# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_order_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=None, null=True, verbose_name='Order / Delivery date'),
        ),
    ]
