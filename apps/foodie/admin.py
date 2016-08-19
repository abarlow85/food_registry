from django.contrib import admin
from .models import Cookbook, Recipe, RecipeCategory
# Register your models here.

admin.site.register(Cookbook)
admin.site.register(Recipe)
admin.site.register(RecipeCategory)