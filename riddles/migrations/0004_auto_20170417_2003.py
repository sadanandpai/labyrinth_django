# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riddles', '0003_userdetails_sublevel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answers',
            name='sublevel',
        ),
        migrations.RemoveField(
            model_name='userdetails',
            name='sublevel',
        ),
    ]
