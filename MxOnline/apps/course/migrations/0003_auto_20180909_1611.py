# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-09 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20180909_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='detail',
            field=models.CharField(default='', max_length=100, verbose_name='课程详情'),
        ),
    ]
