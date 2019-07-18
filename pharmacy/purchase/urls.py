from django.contrib import admin

from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('supply_product',views.Supply_product_list, name='Supply_product_list'),
    path('supply_product_view/<int:pk>', views.Supply_product_view, name='Supply_product_view'),
    path('supply_product_new', views.Supply_product_create, name='Supply_product_new'),
    url(r'^supply_product_edit/(?P<pk>\d+)$', views.Supply_product_update, name='Supply_product_edit'),
    url(r'^supply_product_delete/(?P<pk>\d+)$', views.Supply_product_delete, name='Supply_product_delete'),
    url(r'^ajax_calls/item_search',views.autoComplete_Item),
    url(r'^ajax_calls/supplier_search',views.autoComplete_Supplier),
    url(r'^ajax_calls/supply_product_search',views.Supply_product_search),
    url(r'^ajax_calls/supply_product_save',views.Supply_product_save),
    url(r'^ajax_calls/order_save',views.Order_save),
    path('order',views.Order_list, name='Order_list'),
    path('order_new', views.Order_create, name='Order_new'),
    path('order_view/<int:pk>', views.Order_view, name='Order_view'),
    url(r'^order_edit/(?P<pk>\d+)$', views.Order_update, name='Order_edit'),
    url(r'^order_view/ajax_calls/order_list_save',views.Order_view_edit),
    url(r'^order_delete/(?P<pk>\d+)$', views.Order_delete, name='Order_delete'),
    path('rtr_view/<int:pk>',views.Rtr_order,name='Rtr_view'),
    url(r'^rtr_view/ajax_calls/rtr_order_save',views.Rtr_order_save),
]