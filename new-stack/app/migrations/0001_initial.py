# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(max_length=200, null=True)),
                ('source_name', models.CharField(max_length=200)),
                ('author_name', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('urlToImage', models.CharField(max_length=200)),
                ('publishedAt', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('resident', models.CharField(max_length=200)),
            ],
        ),
    ]
