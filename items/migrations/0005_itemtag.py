# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20150826_1731'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=20)),
                ('item', models.ForeignKey(to='items.Item')),
            ],
        ),
    ]
