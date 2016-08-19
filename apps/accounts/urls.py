from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^register/$', views.Register.as_view(), name='accounts-register'),
	url(r'^login/$', views.Login.as_view(), name='accounts-login'),
	url(r'^logout/$', views.logoff, name='user-logout')
	
]