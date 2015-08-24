# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0003_auto_20150819_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='riot_id',
            field=models.IntegerField(default=1),
        ),
    ]
