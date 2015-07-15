# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product'},
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='order'),
        ),
    ]
