# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 00:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0006_cookbook_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='foodie.RecipeCategory'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]