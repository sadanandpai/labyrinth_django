# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riddles', '0004_auto_20170417_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='level',
            field=models.DecimalField(decimal_places=1, default=1.1, max_digits=2),
        ),
    ]