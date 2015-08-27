# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0005_auto_20150820_1828'),
        ('items', '0002_item_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='counter_hero',
            field=models.ForeignKey(related_name='counter', default=1, to='heroes.Hero'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='for_hero',
            field=models.ForeignKey(default=1, to='heroes.Hero'),
            preserve_default=False,
        ),
    ]
