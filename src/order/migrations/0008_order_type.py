# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20150715_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.CharField(default='Regular', max_length=255, choices=[('Regular', b'Regular'), ('Left with customer', 'Left with customer')]),
        ),
    ]
