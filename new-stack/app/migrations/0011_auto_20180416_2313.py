# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-17 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20180416_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factcheck',
            name='article',
        ),
        migrations.RemoveField(
            model_name='sentiment',
            name='article',
        ),
        migrations.AddField(
            model_name='sentiment',
            name='url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]