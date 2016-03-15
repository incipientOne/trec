# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trec', '0005_auto_20160314_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='run_id',
            field=models.TextField(default='', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='run',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]