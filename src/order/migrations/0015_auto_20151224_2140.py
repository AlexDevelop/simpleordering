# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20151014_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Order / Delivery date'),
        ),
    ]
