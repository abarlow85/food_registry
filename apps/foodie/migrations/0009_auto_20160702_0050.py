# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 00:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0008_auto_20160702_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookbook',
            name='categories',
            field=models.ManyToManyField(blank=True, db_table='cookbooks_have_categories', to='foodie.RecipeCategory'),
        ),
        migrations.AlterField(
            model_name='cookbook',
            name='recipes',
            field=models.ManyToManyField(blank=True, db_table='cookbooks_have_recipes', to='foodie.Recipe'),
        ),
    ]
