# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0005_auto_20150820_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='hero',
            name='tag',
        ),
        migrations.AddField(
            model_name='herotag',
            name='hero',
            field=models.ForeignKey(to='heroes.Hero'),
        ),
    ]
