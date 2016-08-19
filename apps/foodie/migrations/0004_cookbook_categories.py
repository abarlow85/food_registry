# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0003_recipe_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='cookbook',
            name='categories',
            field=models.ManyToManyField(db_table='cookbooks_have_categories', to='foodie.RecipeCategory'),
        ),
    ]