# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trec', '0011_auto_20160315_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='recall01',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall02',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall03',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall04',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall05',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall06',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall07',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall08',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall09',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='run',
            name='recall10',
            field=models.FloatField(blank=True, null=True),
        ),
    ]