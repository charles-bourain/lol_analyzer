# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0002_auto_20150819_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='armor',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='armorperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='attack_damage',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='attack_range',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='attackdamageperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='attackspeedoffset',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='attackspeedperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='crit',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='critperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='hp',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='hpperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='hpregen',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='hpregenperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='movespeed',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='mp',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='mp_per_level',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='mpregen',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='mpregenperlevel',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='riot_id',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='spellblock',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='hero',
            name='spellblockperlevel',
            field=models.FloatField(default=1),
        ),
    ]
