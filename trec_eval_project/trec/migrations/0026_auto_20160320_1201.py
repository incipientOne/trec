# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trec', '0025_auto_20160320_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researcher',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_images/default.png', upload_to='profile_images'),
        ),
    ]
