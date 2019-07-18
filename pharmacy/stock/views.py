from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from items.models import Item
from items.forms import ItemForm
from accounts.models import User
import simplejson
import json

from .forms import StockForm
from .models import Stock
# Create your views here.
def Stock_create(request,template_name='stock/stock_form.html'):
    error_statement = ''
    obj_list = []
    item= Item.objects.all()
    stock_form = StockForm(request.POST or None)
    error = False
    if request.method == "POST":
        if request.POST.get("btn_search"):
            name = request.POST.get('txt_search')
            exist = Item.objects.filter(name=name).exists()
            if not exist:
                error = True
            else:
                item = Item.objects.get(name=name)
        if request.POST.get("submit"):
            if stock_form.is_valid():
                stock = stock_form.save(commit=False)
                name=request.POST.get('name')
                it=Item.objects.get(name=name)
                stock.item_id=it
                stock.save()
                return redirect('Stock_list')

    params = {'obj_list': item, 'error': error, 'stock_form': stock_form}
    return render(request,template_name,params)

def Stock_list(request,template_name='stock/stock_list.html'):
    error=False
    count=1
    error_statement=''
    if request.method == "POST":
        name = request.POST.get('item')
        item=Item.objects.filter(name=name)
        if not item.exists():
            error=True
            error_statement="Item doesn't exist"
        else:
            item=Item.objects.get(name=name)
            stock=Stock.objects.filter(item_id=item.pk)
            if stock.count() == 1:
                stock=Stock.objects.get(item_id=item.pk)
                count=0
        if error:
            stock = Stock.objects.all()
    else:
        stock=Stock.objects.all()
    uname=request.session['username']
    if User.objects.get(username=uname).role == "Worker":
        role = 0
    else:
        role = 1
    params = {'obj_list': stock, 'count':count,'error': error,
              'error_statement': error_statement,'role':role}
    return render(request, template_name, params)


