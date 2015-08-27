# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_auto_20150826_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='counter_hero',
            field=models.ForeignKey(related_name='counter', blank=True, to='heroes.Hero', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='for_hero',
            field=models.ForeignKey(blank=True, to='heroes.Hero', null=True),
        ),
    ]
