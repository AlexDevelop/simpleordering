# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_product_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 15, 12, 52, 18, 284202, tzinfo=utc), verbose_name='order date', auto_created=True),
            preserve_default=False,
        ),
    ]
