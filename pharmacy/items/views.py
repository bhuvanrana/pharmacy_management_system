from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from stock.models import Stock
from accounts.models import User
from django.contrib import messages
# Create your views here.

def Item_create(request,template_name='items/item_form.html'):
    error=False
    error_statement = ''
    item_form = ItemForm(request.POST or None)
    if item_form.is_valid():
        item_name=item_form.cleaned_data.get('name').lower()
        type=item_form.cleaned_data.get('type')
        exist=Item.objects.filter(name=item_name,type=type).exists()
        if not exist:
            new_item=item_form.save(commit=False)
            new_item.name=item_name
            new_item.save()
            return redirect('Item_list')
        else:
            error=True
            error_statement="Item already exists!!"
    params= {'item_form':item_form,'error':error,'error_statement':error_statement}
    return render(request,template_name,params)

def Item_list(request,template_name='items/item_list.html'):
    error=False
    error_stat=''
    count=1
    print("item list")
    if request.method == "POST":
        name = request.POST.get('search')
        item = Item.objects.filter(name__startswith=name)
        if not item.exists():
            error = True
            error_stat="Item doesn't exist"
        else:
            if item.count() == 1:
                item = Item.objects.get(name__startswith=name)
                count=0
    else:
        item = Item.objects.all()
    if error:
        item = Item.objects.all()
    uname = request.session['username']
    if User.objects.get(username=uname).role == "Worker":
        role = 0
    else:
        role = 1
    params = {'obj_list': item, 'error': error,'error_statement':error_stat,'count':count,'role':role}
    return render(request, template_name, params)

def Item_update(request, pk, template_name='items/item_form.html'):
    item= get_object_or_404(Item, pk=pk)
    item_form = ItemForm(request.POST or None,instance = item)
    if item_form.is_valid():
        item=item_form.save(commit=False)
        name=item_form.cleaned_data.get('name')
        name=name.lower()
        item.name=name
        item.save()
        return redirect('Item_list')
    params = {'item_form': item_form}
    return render(request, template_name, params)

def Item_delete(request, pk, template_name='items/item_confirm_delete.html'):
    item= get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        if request.POST.get("btn_delete"):
            print("post method of itemdelete")
            item.delete()
            return redirect('Item_list')
        if request.POST.get("submit"):
            return redirect('Item_list')
    count=1
    print("dfgh")
    if Stock.objects.filter(item_id=item).exists():
        print("here")
        error=True
        error_stat="Stock for this item exists.... Can't delete it at the moment"
        item=Item.objects.all()
        params = {'obj_list': item, 'error': error,'error_statement':error_stat, 'count': count}
        return render(request,'items/item_list.html', params)
    else:
        return render(request, template_name, {'object':item})
