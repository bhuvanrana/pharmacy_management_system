from django.contrib import admin

from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    path('sales',views.Sales_list, name='Sales_list'),
    path('sales_new', views.Sales_create, name='Sales_new'),
    url(r'^ajax_calls/item_search',views.autoComplete_Item),
    url(r'^ajax_calls/stock_search',views.Stock_batch_search),
    url(r'^ajax_calls/sale_save',views.Sale_save),
   path('sales_view/<int:pk>', views.Sales_view, name='Sales_view'),
   # url(r'^sales_edit/(?P<pk>\d+)$', views.Sales_update, name='Sales_edit'),
 #   url(r'^order_view/ajax_calls/order_list_save',views.Order_view_edit),
  #  url(r'^order_delete/(?P<pk>\d+)$', views.Order_delete, name='Order_delete'),
  #  url('rtr_order_view/<int:pk>',views.Rtr_order,name='Rtr_order_view'),
  #  url(r'^order_view/ajax_calls/rtr_order_save',views.Rtr_order_save),
]