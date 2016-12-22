from django.conf.urls import url
from todolist import views
urlpatterns = [
    url(r'^$', views.todolist, name='todolist'),
    url(r'^todolist/$', views.todolist, name='todolist'),
    url(r'^add_todolist/$', views.add_todolist, name='add_todolist'),
    url(r'^del_todolist/$', views.del_todolist, name='del_todolist'),
    url(r'^edit_todolist/$', views.edit_todolist, name='edit_todolist'),
    url(r'^chk_todolist/$', views.chk_todolist, name='chk_todolist'),
]