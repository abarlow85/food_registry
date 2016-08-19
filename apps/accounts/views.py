from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

from django.views.generic import View

from .forms import RegisterForm 
from ..foodie.models import Cookbook, RecipeCategory
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class Register(View):
	def post(self, request):
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				c = Cookbook.objects.create(user=user)
				login(request, user)
				return JsonResponse({'status': True, 'user':user.id}, safe=False)
			else:
				return JsonResponse({'status': False})
		else:
			return JsonResponse({'errors':form.errors.as_json()}, safe=False)

class Login(View):
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse({'status': True, 'user':user.id}, safe=False)
		else:
			return JsonResponse({'errors': 'Invalid credentials'})

def logoff(request):
	if request.user.is_authenticated():
		print 'logging out'
		logout(request)
		return HttpResponseRedirect('/')
	else:
		return JsonResponse({'status': True});

