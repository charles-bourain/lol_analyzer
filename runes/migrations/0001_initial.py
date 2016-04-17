# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rune',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runeId', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=10000)),
                ('name', models.SlugField(max_length=1000)),
            ],
        ),
    ]
