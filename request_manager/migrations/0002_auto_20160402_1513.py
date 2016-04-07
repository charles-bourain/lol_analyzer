# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RequestManager',
            new_name='Request',
        ),
    ]
