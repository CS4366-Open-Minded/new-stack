# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-17 03:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180416_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentiment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Article'),
        ),
    ]
