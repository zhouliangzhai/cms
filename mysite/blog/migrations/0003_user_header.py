# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-09 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='header',
            field=models.CharField(default='/static/img/default.png', max_length=255, verbose_name='用户头像'),
        ),
    ]
