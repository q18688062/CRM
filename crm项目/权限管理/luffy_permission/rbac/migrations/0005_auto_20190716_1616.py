# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-16 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0004_permission_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='别名'),
        ),
    ]
