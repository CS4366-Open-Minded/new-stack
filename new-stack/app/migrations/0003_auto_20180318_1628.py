# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 21:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180318_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='resident',
            new_name='residence',
        ),
    ]
