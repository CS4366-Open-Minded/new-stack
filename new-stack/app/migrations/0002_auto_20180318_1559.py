# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-18 20:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author_name',
            new_name='author_Name',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='publishedAt',
            new_name='published_On',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='source_id',
            new_name='source_ID',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='source_name',
            new_name='source_Name',
        ),
        migrations.RenameField(
            model_name='article',
            old_name='urlToImage',
            new_name='url_To_Image',
        ),
    ]
