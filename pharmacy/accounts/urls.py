from django.contrib import admin

from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('worker', views.worker_homepage, name='Worker_homepage'),
    path('login',views.authentication,name='index'),
    path('list', views.User_list, name='User_list'),
    path('new', views.User_create, name='User_new'),
    url(r'^edit/(?P<pk>\d+)$', views.User_update, name='User_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.User_delete, name='User_delete'),
    path('supplier', views.Supplier_list, name='Supplier_list'),
    path('new_supplier', views.Supplier_create, name='Supplier_new'),
    url(r'^edit_supplier/(?P<pk>\d+)$', views.Supplier_update, name='Supplier_edit'),
    url(r'^delete_supplier/(?P<pk>\d+)$', views.Supplier_delete, name='Supplier_delete'),
    path('change_pwd',views.Change_pwd,name='Change_pwd'),
    path('logout',views.Logout,name="logout"),
]