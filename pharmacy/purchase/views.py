from accounts.forms import SupplierForm
from accounts.models import Supplier
import simplejson
import json
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from items.models import Item
from items.forms import ItemForm
import logging
from .forms import Supply_productForm,OrderForm,Order_itemsForm
from .models import Supply_product,Order,Order_items
from stock.models import Stock
from accounts.models import User
# Create your views here.
def Supply_product_create(request,template_name='purchase/supply_product_form.html'):
    return render(request,template_name)

def Supply_product_save(request):
    data=""
    if request.is_ajax():
        print("reached to save")
        json_dict = request.GET.get('abc')
        json_dict = json.loads(str(json_dict))
        item_id = json_dict['item_id']
        discount = json_dict['discount']
        sid = json_dict['sid']
        purchase=json_dict['purchase']
        it=Item.objects.get(id=item_id)
        print(it.name)
        supplier=Supplier.objects.get(id=sid)
        print(supplier.name)
        if not Supply_product.objects.filter(item_id=it,supplier_id=supplier).exists():
            print("creating ")
            Supply_product.objects.create(item_id=it,supplier_id=supplier,
                                          purchase_price=purchase,discount=discount)
            print("saved")
        else:
            data = "It already exits!!"
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)

def Supply_product_list(request,template_name='purchase/supply_product_list.html'):
    error=False
    count=1
    error_statement=''
    if request.method == "POST":
        name = request.POST.get('item')
        exist=Item.objects.filter(name=name).exists()
        if not exist:
            error=True
            error_statement="Item doesn't exist"
        else:
            item=Item.objects.get(name=name)
            supply_product=Supply_product.objects.filter(item_id=item.pk)
            if supply_product.count() == 1:
                supply_product=Supply_product.objects.get(item_id=item.pk)
                count=0
        if error:
            supply_product = Supply_product.objects.all()
    else:
        supply_product=Supply_product.objects.all()
    uname = request.session['username']
    if User.objects.get(username=uname).role == "Worker":
        role = 0
    else:
        role = 1
    params = {'obj_list': supply_product, 'error': error,
              'error_statement': error_statement,'count':count,'role':role}
    return render(request, template_name, params)


def Supply_product_view(request, pk, template_name='purchase/supply_product_detail.html'):
    sp= get_object_or_404(Supply_product, pk=pk)
    return render(request, template_name, {'obj':sp})


def Supply_product_update(request, pk, template_name='purchase/supply_product_update.html'):
    sp= get_object_or_404(Supply_product, pk=pk)
    error=False
    error_stat=''
    sp_form = Supply_productForm(request.POST or None, instance=sp)
    if request.method == "POST":
        if sp_form.is_valid() :
            mrp=request.POST.get('mrp')
            purchase=request.POST.get('purchase_price')
            if purchase > mrp:
                error=True
                error_stat="Purchase Price is greater than mrp.... Changes are not saved"
            else:
                sp.save()
                return redirect('Supply_product_list')
    params = {'obj':sp,'supply_product_form':sp_form,'error':error,'error_stat':error_stat}
    return render(request, template_name, params)

def Supply_product_delete(request, pk, template_name='purchase/supply_product_confirm_delete.html'):
    sp= get_object_or_404(Supply_product, pk=pk)
    if request.method == "POST" :
        sp.delete()
        return redirect('Supply_product_list')
    return render(request, template_name, {'object':sp})


def Order_create(request,template_name = 'purchase/order_form.html'):
    order_items_form = Order_itemsForm()
    params = {'form': order_items_form}
    return render(request, template_name, params)

def Order_save(request):
    print("sdubfvu")
    data=[]
    if request.is_ajax():
        print(request)
        json_dict = request.GET.get('abc')
        json_dict=json.loads(str(json_dict))
        objects=json_dict['objects']
        date=json_dict['date']
        supplier_id=json_dict['supplier_id']
        print("Supplier id "+ str(supplier_id))
        supplier=Supplier.objects.get(id=supplier_id)
        gtotal=json_dict['gtotal']
        order=Order.objects.create(supplier_id=supplier,gtotal=gtotal,date=date)
        print("order getting saved with order id "+ str(order.id))
        print(objects)
        for i in objects:
            print(i)
            item=Item.objects.get(id=i['item_id'])
            obj=Order_items.objects.create(order_id=order,item_id=item,
                                           quantity_ordered=i['qty'],mrp=i['mrp'],
                                           purchase_price=i['purchase_price'],
                                           discount=i['discount'])
            print(obj)
            print("obj gets saved")
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)

def autoComplete_Item(request):
    if request.is_ajax():
        q = request.GET.get('term', '').lower()
        print("values received  " +q)
        search_qs = Item.objects.filter(name__startswith=q)
        print (search_qs)
        results = []
        print ("here")
        for r in search_qs:
            obj=[]
            obj.append(r.id)
            obj.append(r.name)
            obj.append(r.manufacturer)
            obj.append(r.description)
            obj.append(r.discount)
            obj.append(r.MRP)
            obj.append(r.type)
            results.append(obj)
        data = simplejson.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)


def autoComplete_Supplier(request):
    if request.is_ajax():
        q = request.GET.get('term', '').lower()
        print("values received  " + q)
        search_qs = Supplier.objects.filter(name__startswith=q)
        results = []
        print("here")
        for r in search_qs:
            obj = []
            obj.append(r.id)
            obj.append(r.name)
            obj.append(r.address)
            obj.append(r.phone_no)
            results.append(obj)
        data = simplejson.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)
def Supply_product_search(request):
    print("in supply product search")
    if request.is_ajax():
        item_id = request.GET.get('item_id')
        supplier_id=request.GET.get('supplier_id')
        print("values received  " + str(item_id)+" supplier id "+ str(supplier_id))
        search_qs = Supply_product.objects.filter(item_id=item_id,supplier_id=supplier_id)
        search_item=Item.objects.get(id=item_id)
        if search_qs.exists():
            search_qs=Supply_product.objects.get(item_id=item_id,supplier_id=supplier_id)
            print("exists")
            results = []
            print("here")
            results.append(search_qs.purchase_price)
            results.append(search_item.MRP)
            results.append(search_qs.discount)
            data = simplejson.dumps(results)
            print(data)
        else:
            res=[]
            print("empty passed")
            data=simplejson.dumps(res)
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)


def Order_list(request,template_name='purchase/order_list.html'):
    error=False
    count=1
    if request.method == "POST":
        name = request.POST.get('search').lower()
        supplier = Supplier.objects.filter(name=name)
        if not supplier.exists():
            error = True
        else:
            supplier=Supplier.objects.get(name=name)
            supplier_order = Order.objects.filter(supplier_id=supplier.id).order_by('-date')
            if supplier_order.count() == 1:
                count=0
                supplier_order = Order.objects.get(supplier_id=supplier.id)
    else:
        supplier_order = Order.objects.all().order_by('-date')
    if error:
        supplier_order = Order.objects.all().order_by('-date')
    uname = request.session['username']
    if User.objects.get(username=uname).role == "Worker":
        role = 0
    else:
        role = 1
    params = {'order': supplier_order, 'error': error,'count':count,'role':role}
    return render(request, template_name, params)

def Order_view(request, pk, template_name='purchase/order_detail.html'):
    order= get_object_or_404(Order, pk=pk)
    count=1
    order_items=Order_items.objects.filter(order_id=order.id)
    if order_items.count() == 1:
        count=0
        order_items=Order_items.objects.get(order_id=order.id)
    return render(request, template_name, {'order':order_items,'count':count})


def Order_update(request, pk, template_name='purchase/order_edit.html'):
    order= get_object_or_404(Order, pk=pk)
    order_form = ItemForm(request.POST or None,instance = order)
    if item_form.is_valid():
        item=item_form.save(commit=False)
        name=item_form.cleaned_data.get('name')
        name=name.lower()
        item.name=name
        item.save()
        return redirect('Item_list')
    params = {'item_form': item_form}
    return render(request, template_name, params)

def Order_view_edit(request):
    data = []
    print("HIII")
    if request.is_ajax():
        json_dict = request.GET.get('abc')
        json_dict = json.loads(str(json_dict))
        arr_edit = json_dict['arr_edit']
        order_id = json_dict['order_id']
        arr_del = json_dict['arr_del']
        order = Order.objects.get(id=order_id)
        gtotal = float(order.gtotal)
        for item in arr_edit:
            order_item=Order_items.objects.get(order_id=order,item_id=Item.objects.get(id=item['item_id']))
            print(order_item)
            qty=order_item.quantity_ordered
            price=float(order_item.purchase_price)
            gtotal-=qty*price
            gtotal+=float(item['qty'])*price
            order_item.quantity_ordered=item['qty']
            order_item.save()
            print("edit changes got saved")
        count=0
        item_count=Order_items.objects.all().count()
        print("item count"+ str(item_count))
        for item_id in arr_del:
            order_item=Order_items.objects.get(order_id=order,item_id=Item.objects.get(id=item_id))
            count=count+1
            qty = order_item.quantity_ordered
            price = float(order_item.purchase_price)
            gtotal -= qty * price
            order_item.delete()
            print("del changes got saved")
        order.gtotal=gtotal
        order.save()
        print("count"+ str(count))
        if item_count==count:
            order.delete()
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)

def Order_delete(request, pk, template_name='purchase/supply_product_confirm_delete.html'):
    order= get_object_or_404(Order, pk=pk)
    if request.method == "POST" :
        order.delete()
        return redirect('../order')
    return render(request, template_name, {'object':order})

def Rtr_order(request, pk, template_name='purchase/retreive_order_detail.html'):
    order= get_object_or_404(Order, pk=pk)
    print("order rtr")
    order_items=Order_items.objects.filter(order_id=order.id)
    if order_items.count()>1:
        count=1
    else:
        count=0
        order_items=Order_items.objects.get(order_id=order.id)
    return render(request, template_name, {'order':order_items,'count':count})

def Rtr_order_save(request):
    data = []
    print("retrev order save")
    if request.is_ajax():
        json_dict = request.GET.get('abc')
        json_dict = json.loads(str(json_dict))
        arr_save= json_dict['arr_save']
        order_id = json_dict['order_id']
        order = Order.objects.get(id=order_id)
        for item in arr_save:
            a=Item.objects.get(id=item['item_id'])
            stock=Stock.objects.filter(item_id=a,batch_no=item['batchno'])
            order_item = Order_items.objects.filter(order_id=order, item_id=a,batchno__isnull=True)
            qty = int(item['qty'])
            batchno=item['batchno']
            exp_date=item['exp_date']
            if order_item.exists():
                order_item=Order_items.objects.get(order_id=order, item_id=a,batchno__isnull=True)
                order_item.quantity_ordered=qty
                order_item.batchno=batchno
                order_item.exp_date=exp_date
                order_item.save()
            else:
                order_item=Order_items.objects.create(order_id=order,item_id=a,batchno=batchno,quantity_ordered=qty,
                                   purchase_price=item['purchase_price'],discount=float(item['discount']),
                                   mrp=item['mrp'],exp_date=exp_date)
            print("edit changes got saved")
            a.total_no_of_units += order_item.quantity_ordered
            a.save()
            if stock.exists():
                stock = Stock.objects.get(item_id=a, batch_no=item['batchno'])
                stock.no_of_units = stock.no_of_units + order_item.quantity_ordered
                stock.save()
            else:
                Stock.objects.create(item_id=a,batch_no=batchno,no_of_units=qty,
                                     exp_date=exp_date,mrp=item['mrp'])
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)