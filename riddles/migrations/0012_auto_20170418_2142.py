# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riddles', '0011_userdetails_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='level',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
