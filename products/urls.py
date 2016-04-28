from django.conf.urls import include, url
from .views import index_view, details_view, review_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^(?P<id>\d+)$', details_view, name='details'),
 	url(r'^(?P<id>\d+)/review$', review_view, name='review'),
    # url(r'^accounts/logout/$', auth_views.logout), 
    # url(r'^accounts/login/$', auth_views.login, {'template_name': 'admin/login.html'}), 
    # url(r'^accounts/$', 'django.views.generic.simple.redirect_to', {'url': '/'}), 
    # url(r'^accounts/profile/$', 'django.views.generic.simple.redirect_to', {'url': '/'}),
]
