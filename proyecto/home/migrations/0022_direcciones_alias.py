# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-27 04:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_cart_direccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='direcciones',
            name='alias',
            field=models.CharField(max_length=50, null=True),
        ),
    ]