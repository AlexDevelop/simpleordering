# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='housenumber_addition',
            field=models.CharField(default=b'', max_length=10, null=True, verbose_name='housenumber addition'),
        ),
    ]
