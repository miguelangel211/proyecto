# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-30 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20171130_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='fallo',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
