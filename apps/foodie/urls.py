from django.conf.urls import url
from . import views

urlpatterns = [
	
	url(r'^$', views.Index.as_view()),
	url(r'^recipes/$', views.get_recipes),
	url(r'^recipes/(?P<pk>\w+)$', views.get_one_recipe),
	url(r'^cookbooks$', views.GetOrUpdateCookbook.as_view()),
	url(r'^cookbooks/(?P<pk>\w+)$', views.ReadOrRemoveRecipe.as_view()),
]