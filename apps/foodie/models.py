from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class RecipeCategory(models.Model):
	category = models.CharField(max_length=255)

	class Meta:
		db_table = 'categories'
		ordering = ['category']
	def __str__(self):
		return self.category

class Recipe(models.Model):
	recipe_id = models.CharField(max_length=140)
	title = models.CharField(max_length=255)
	image_url = models.URLField(default='https://pixabay.com/static/uploads/photo/2016/01/18/16/20/food-1146822_960_720.jpg')
	notes = models.TextField(blank=True)
	category = models.ForeignKey(RecipeCategory, on_delete=models.SET_NULL, null=True)
	class Meta:
		db_table = 'recipes'
		ordering = ['title']
	def __str__(self):
		return self.title

class Cookbook(models.Model):
	user = models.ForeignKey(User, default=1)
	categories = models.ManyToManyField(RecipeCategory, db_table="cookbooks_have_categories")
	recipes = models.ManyToManyField(Recipe, db_table="cookbooks_have_recipes", blank=True)
