# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-03 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0013_cookbook_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookbook',
            name='categories',
            field=models.ManyToManyField(db_table='cookbooks_have_categories', default=4, to='foodie.RecipeCategory'),
        ),
    ]
