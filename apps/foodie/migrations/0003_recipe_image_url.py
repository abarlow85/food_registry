# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 22:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0002_cookbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image_url',
            field=models.URLField(default='https://pixabay.com/static/uploads/photo/2016/01/18/16/20/food-1146822_960_720.jpg'),
        ),
    ]