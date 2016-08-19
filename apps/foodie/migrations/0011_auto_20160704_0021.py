# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 00:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0010_cookbook_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookbook',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]