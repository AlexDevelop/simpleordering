# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20150715_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='fullname')),
                ('postalcode', models.CharField(max_length=8, verbose_name='postalcode')),
                ('housenumber', models.CharField(max_length=10, verbose_name='housenumber')),
                ('housenumber_addition', models.CharField(default=None, max_length=10, null=True, verbose_name='housenumber addition')),
            ],
            options={
                'verbose_name': 'Customer',
            },
        ),
    ]
