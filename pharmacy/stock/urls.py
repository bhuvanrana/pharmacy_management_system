from django.contrib import admin

from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('list',views.Stock_list, name='Stock_list'),

]