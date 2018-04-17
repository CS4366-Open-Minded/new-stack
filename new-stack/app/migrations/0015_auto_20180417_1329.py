# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-17 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180417_0153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='sentimentResult',
        ),
        migrations.AddField(
            model_name='article',
            name='sentimentNeg',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='sentimentNeu',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='sentimentPos',
            field=models.CharField(max_length=100, null=True),
        ),
    ]