from django.conf.urls import include, url
from .views import index_view

urlpatterns = [
    url(r'^$', index_view, name='index'),
]
