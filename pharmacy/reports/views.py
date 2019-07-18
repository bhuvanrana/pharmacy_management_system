from django.shortcuts import render
from items.models import Item
from stock.models import Stock
import datetime
from stock.models import Stock
from django.db.models import Count,Sum
from purchase.models import Order
from django.db.models.functions import TruncMonth
# Create your views here.



def Exp_date_list(request,template_name='reports/exp_date_list.html'):
    curr_date = datetime.date.today()
    new_date = curr_date + datetime.timedelta(days=5000)
    stock = Stock.objects.filter(exp_date__range=[curr_date, new_date])
    params={'stock':stock}
    return render(request,template_name,params)

def Min_qty_list(request,template_name='reports/min_qty_list.html'):
    item=Item.objects.all()
    return render(request,template_name,{'item':item})

def monthly_order(request,template_name='reports/monthly_order_list.html'):
    curr_date=datetime.date.today()
    month=curr_date.month

    order=Order.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('gtotal'))
    print(order)
    return render(request,template_name,{'monthly_list':order})


