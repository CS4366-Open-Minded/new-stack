# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-02 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_factcheck_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factcheck',
            name='URLFact',
            field=models.URLField(max_length=254, null=True),
        ),
    ]
