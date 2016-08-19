# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cookbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ManyToManyField(db_table='cookbooks_have_recipes', to='foodie.Recipe')),
            ],
        ),
    ]