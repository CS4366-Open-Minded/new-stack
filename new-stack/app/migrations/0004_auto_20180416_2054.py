# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-17 01:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_factcheck'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factcheck',
            old_name='factURL',
            new_name='URLFact',
        ),
    ]