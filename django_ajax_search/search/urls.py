from django.conf.urls import url, include
from search import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^match$', views.match, name='match'),
]
