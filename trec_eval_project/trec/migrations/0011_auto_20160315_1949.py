# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trec', '0010_run_recal00'),
    ]

    operations = [
        migrations.RenameField(
            model_name='run',
            old_name='recal00',
            new_name='recall00',
        ),
    ]