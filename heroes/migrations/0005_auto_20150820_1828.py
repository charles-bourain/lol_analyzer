# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0004_auto_20150819_1951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hero',
            old_name='attack_damage',
            new_name='attackdamage',
        ),
        migrations.RenameField(
            model_name='hero',
            old_name='attack_range',
            new_name='attackrange',
        ),
        migrations.RenameField(
            model_name='hero',
            old_name='mp_per_level',
            new_name='mpperlevel',
        ),
    ]
