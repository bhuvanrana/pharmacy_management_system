from django.shortcuts import render,redirect, get_object_or_404
from .models import Invoice,Invoice_items
from items.models import Item
from stock.models import Stock
from accounts.models import User
import simplejson
import json,datetime
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
def Sales_list(request,template_name='sales/sales_list.html'):
    sales = Invoice.objects.all().order_by('-date')
    params = {'sales': sales}
    uname=request.session['username']
    if User.objects.get(username=uname).role == "Worker":
        role = 0
    else:
        role = 1
    params={'role':role,'sales':sales}
    return render(request, template_name, params)

def Sales_create(request,template_name='sales/sales_form.html'):
    return render(request, template_name)


def autoComplete_Item(request):
    if request.is_ajax():
        q = request.GET.get('term', '').lower()
        print("values received  " +q)
        search_qs = Item.objects.filter(name__startswith=q)
        results = []
        print ("here")
        for r in search_qs:
            obj=[]
            obj.append(r.id)
            obj.append(r.name)
            obj.append(r.discount)
            obj.append(r.type)
            obj.append(r.per_unit)
            results.append(obj)
        data = simplejson.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)

def myconverter(o):
    if isinstance(o, datetime.date):
        return o.isoformat()

def Stock_batch_search(request):
    if request.is_ajax():
        item_id = int(request.GET.get('item_id'))
        item=Item.objects.get(id=item_id)
        stock=Stock.objects.filter(item_id=item)
        results=[]
        if stock.exists():
            for i in stock:
                obj=[]
                obj.append(i.no_of_units)
                obj.append(i.loose_qty)
                obj.append(i.batch_no)
                obj.append(i.exp_date)
                obj.append(i.mrp)
                results.append(obj)
            print(results)
            data = simplejson.dumps(results,default=myconverter)
            print(data)
        else:
            print("empty passed")
            data = simplejson.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)



def Sale_save(request):
    data = []
    print("sale save")
    if request.is_ajax():
        json_dict = request.GET.get('abc')
        json_dict = json.loads(str(json_dict))
        c_name = json_dict['c_name']
        c_phone = json_dict['c_phone']
        date = json_dict['date']
        gtotal = float(json_dict['gtotal'])
        objects=json_dict['objects']
        invoice=Invoice.objects.create(c_name=c_name,c_phone=c_phone,date=date,gtotal=gtotal)
        for item in objects:
            a = Item.objects.get(id=item['item_id'])
            stock = Stock.objects.get(item_id=a, batch_no=item['batchno'])
            qty = int(item['qty'])
            per_unit=a.per_unit
            no_of_units = qty// per_unit
            loose = qty % per_unit
            stock.no_of_units -= no_of_units
            if  loose > stock.loose_qty :
                stock.no_of_units -= 1
                stock.loose_qty += per_unit
            stock.loose_qty -= loose
            a.total_no_of_units -= no_of_units
            if loose > a.total_loose_qty:
                a.total_no_of_units -=1
                a.total_loose_qty += per_unit
            a.total_loose_qty -= loose

            if a.total_loose_qty> per_unit:
                a.total_no_of_units += a.total_loose_qty // per_unit
                a.total_loose_qty = a.total_loose_qty % per_unit

            if stock.loose_qty > per_unit:
                stock.no_of_units += stock.loose_qty // per_unit
                stock.loose_qty = stock.loose_qty % per_unit
            stock.save()
            a.save()
            batchno = item['batchno']
            exp_date = stock.exp_date
            invoice_item = Invoice_items.objects.create(invoice_id=invoice, item_id=a, batchno=batchno,
                                                        no_of_units=no_of_units,loose_qty=loose,
                                                        mrp=stock.mrp,
                                                        discount=float(item['discount']),
                                                        exp_date=exp_date)
            print("edit changes got saved")
            if stock.no_of_units == 0 and stock.loose_qty == 0 :
                stock.delete()
    else:
        data = 'fail'
    mimetype = 'application/simplejson'
    return HttpResponse(data, mimetype)

class initialiser:
    def __init__(self,id,name,n,l,p,exp,b,d,mrp):
        self.id=id
        self.item_name=name
        self.qty=n*p+l
        self.batchno=b
        self.discount=d
        self.exp_date=exp
        self.mrp=mrp

def Sales_view(request,pk, template_name='sales/sales_view.html'):
    print("here")
    invoice = get_object_or_404(Invoice, pk=pk)
    print("in sales view")
    invoice_items=Invoice_items.objects.filter(invoice_id=invoice.id)
    res=[]
    print("starting loop")
    for i in invoice_items:
        obj=initialiser(i.id,i.item_id.name,i.no_of_units,i.loose_qty,i.item_id.per_unit,
                        i.exp_date,i.batchno,i.discount,i.mrp)
        print(obj)
        res.append(obj)
    print(res)
    return render(request, template_name, {'invoice_items':res,'count':1})
