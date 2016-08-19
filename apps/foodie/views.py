from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.core import serializers
import json
import requests

from django.views.generic import View
from ..accounts.forms import RegisterForm

from .api import Food2ForkAPI
from .models import Recipe, RecipeCategory, Cookbook



# Create your views here.

class Index(View):
	template = 'foodie/index.html'
	# context = {'register_form' :RegisterForm()}
	def get(self, request):
		context = {'register_form' :RegisterForm()}
		if request.user.is_authenticated():
			c = Cookbook.objects.get(user=request.user.id)
			context['categories'] = [obj for obj in c.categories.values()]
		return render(request, self.template, context)

def get_recipes(request):
	params = request.GET.values()[0]
	api = Food2ForkAPI()
	url = api.search(params)
	results = requests.get(url).json()

	return JsonResponse(results)

@csrf_exempt
def get_one_recipe(request, pk):
	api = Food2ForkAPI()
	url = api.getOne(pk)
	results = requests.get(url).json()
	return JsonResponse(results)

@method_decorator(csrf_exempt, 'dispatch')
class GetOrUpdateCookbook(View):

	def get(self, request):
		query_set = Cookbook.objects.get(user=request.user.id)
		json = {'categories': [], 'recipes': [obj for obj in query_set.recipes.values()]}

		cat = [obj for obj in query_set.categories.values()]
		for c in cat:
			for r in json['recipes']:
				if c['id'] == r['category_id']:
					json['categories'].append(c)
					break

		return JsonResponse(json)
	def post(self, request):
		client_data = json.loads(request.body);

		r = Recipe()
		r.recipe_id = client_data['recipe_id']
		r.title = client_data['title']
		r.image_url =  client_data['image_url']
		r.notes = client_data['notes']

		def get_or_save_category(category_string):
			try:
				query = RecipeCategory.objects.get(category__iexact=category_string)
				return query
			except Exception, e:
				new_category = RecipeCategory(category=category_string)
				new_category.save()
				return new_category
		r.category = get_or_save_category(client_data['category'].capitalize())
		r.save()

		c = Cookbook.objects.get(user=request.user.id)
		c.categories.add(r.category)
		c.recipes.add(r)
		
		cat = [ob for ob in c.categories.values()]

		rec = [ob for ob in c.recipes.values()]

		pop_cat = []

		for c in cat:
			for r in rec:
				if c['id'] == r['category_id']:
					pop_cat.append(c)
					break

		return JsonResponse({'recipes':rec, 'categories':pop_cat})

	
	def put(self, request):
		client_data = json.loads(request.body);

		r = Recipe()
		r.recipe_id = client_data['recipe_id']
		r.title = client_data['title']
		r.image_url =  client_data['image_url']
		r.notes = client_data['notes']

		def get_or_save_category(category_string):
			try:
				query = RecipeCategory.objects.get(category__iexact=category_string)
				return query
			except Exception, e:
				new_category = RecipeCategory(category=category_string)
				new_category.save()
				return new_category

		r.category = get_or_save_category(client_data['category'])
		r.save()

		c = Cookbook.objects.get(user=request.user.id)
		c.categories.add(r.category)
		c.recipes.add(r)
		
		cat = [ob for ob in c.categories.values()]

		rec = [ob for ob in c.recipes.values()]

		pop_cat = []

		for c in cat:
			for r in rec:
				if c['id'] == r['category_id']:
					pop_cat.append(c)
					break

		return JsonResponse({'recipes':rec, 'categories':pop_cat})

@method_decorator(csrf_exempt, 'dispatch')
class ReadOrRemoveRecipe(View):
	def get(self, request, pk):
		print pk
		r = Recipe.objects.get(id=pk)
		if r is not None:
			return HttpResponseRedirect('/recipes/'+r.recipe_id)
		return JsonResponse({'error': 'Recipe does not exist'})

	def delete(self, request, pk):
		r = Recipe.objects.get(id=pk)
		if r is not None:
			r.delete()
			c = Cookbook.objects.get(user=request.user.id)
			cat = [ob for ob in c.categories.values()]
			rec = [ob for ob in c.recipes.values()]
			pop_cat = []
			for c in cat:
				for r in rec:
					if c['id'] == r['category_id']:
						pop_cat.append(c)
						break

			return JsonResponse({'categories':pop_cat, 'reset_cat': len(pop_cat)})

		return JsonResponse({'error': 'Recipe does not exist'})

