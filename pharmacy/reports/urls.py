from django.contrib import admin

from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('exp_date_view',views.Exp_date_list,name='Exp_date_view'),
    path('min_qty_view',views.Min_qty_list,name='Min_qty_view'),
    path('yearly_order_list',views.monthly_order,name='Monthly_order')

]