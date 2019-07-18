from django.contrib import admin

from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('list',views.Item_list, name='Item_list'),
    path('new', views.Item_create, name='Item_new'),
   url(r'^edit/(?P<pk>\d+)$', views.Item_update, name='Item_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.Item_delete, name='Item_delete'),
]