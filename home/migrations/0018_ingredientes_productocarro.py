# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 00:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20171126_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientes',
            name='productocarro',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.productocarro'),
        ),
    ]
