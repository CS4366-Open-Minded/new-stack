# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-30 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180318_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
