from django.conf.urls import patterns, url
from status import views

urlpatterns = patterns('',
	url(r'^ups$', views.ups_status, name='ups_status'),
	url(r'^tor$', views.tor_status, name='tor_status'),
)
