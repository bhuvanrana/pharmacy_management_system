from django.shortcuts import render,redirect, get_object_or_404
from .models import User,Supplier
import datetime
from django.db.models.functions import TruncMonth
from django.db.models import Count,Sum
from .forms import UserForm,SupplierForm,User_updateForm
from items.models import Item
from stock.models import Stock
from purchase.models import Order
from sales.models import Invoice
# Create your views here.
def authentication(request):
    error = False
    if request.method=="GET":
        return render(request, 'accounts/index.html')
    if request.method=="POST":
        uname = request.POST.get('uname')
        pwd = request.POST.get('password')
        exist = User.objects.filter(username = uname).exists()
        print ( exist )
        if exist :
            obj = User.objects.get(username = uname)
            if obj.password == pwd :
                print("correct pwd")
                request.session['username'] = uname
                if obj.role == "Worker":
                    return redirect('/accounts/worker')
                return redirect('/accounts')
        error = True
        return render(request,'accounts/index.html',{'error':error})


def User_list(request, template_name='accounts/user_list.html'):
    count=1
    if request.method=="POST":
        name=request.POST.get('search').lower()
        user=User.objects.filter(f_name__startswith=name)
        if user.count() == 1 :
            user=User.objects.get(f_name__startswith=name)
            count=0
            print("here")
            print(user.f_name)
            print(user.id)
    else:
        user= User.objects.all()
    uname=request.session['username']
    if User.objects.get(username=uname).role == "Worker":
        role=0
    else:
        role=1

    data = {'object_list':user, 'supplier':False,'count':count,'role':role}
    return render(request, template_name, data)


def User_create(request, template_name='accounts/user_form.html'):
    error=False
    error_statement = ''
    form = UserForm(request.POST or None)
    if form.is_valid():
        print("jiid")
        user=form.save(commit=False)
        phone=form.cleaned_data.get("phone_no")
        pwd = form.cleaned_data.get("password")
        c_pwd = form.cleaned_data.get("confirm_password")
        user.f_name=user.f_name.lower()
        user.l_name=user.l_name.lower()
        username=user.username
        if User.objects.filter(username=username).exists():
            error_statement="Username already exists!!\n Try something else"
            error=True
            print("state: " + error_statement)
        if len(str(phone)) != 10 or not str(phone).isdigit():
            error_statement = "Invalid Phone number"
            error = True
            print("condition")
        if pwd != c_pwd:
            error_statement = "Password fields don't match"
            error = True
        if not error:
            form.save()
            return redirect("User_list")
    else:
        print("form not validated")
    print("error="+ str(error))
    print("state: "+ error_statement)
    params = {'form': form, 'error': error, 'error_statement': error_statement}
    return render(request, template_name, params)

def User_update(request, pk, template_name='accounts/user_form.html'):
    user= get_object_or_404(User, pk=pk)
    error=False
    error_statement=''
    form = User_updateForm(request.POST or None,instance=user)
    if form.is_valid():
        u=form.save(commit=False)
        u.f_name=u.f_name.lower()
        u.l_name=u.l_name.lower()
        phone=u.phone_no
        length=len(str(phone))
        print(len(str(phone)))
        if length != 10 or not phone.isdigit():
            error_statement = "Invalid phone number"
            error = True
        else:
            u.save()
            return redirect('User_list')
    return render(request, template_name, {'form':form,'error':error,
                                           'error_statement':error_statement})

def User_delete(request, pk, template_name='accounts/user_confirm_delete.html'):
    user= get_object_or_404(User, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('User_list')
    return render(request, template_name, {'object':user})

def Supplier_list(request, template_name='accounts/user_list.html'):
    count=1
    if request.method=="POST":
        name=request.POST.get('search').lower()
        user=Supplier.objects.filter(name__startswith=name)
        if user.count() == 1 :
            user=Supplier.objects.get(name__startswith=name)
            count=0
    else:
        user = Supplier.objects.all()
    data = {'object_list':user,'supplier':True,'count':count}
    return render(request, template_name, data)


def Supplier_create(request, template_name='accounts/user_form.html'):
    error=False
    error_statement = ''
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        supp=form.save(commit=False)
        phone=supp.phone_no
        if len(str(phone)) != 10:
            error_statement = "Invalid Phone number"
            error = True
        if not error:
            supp.name=supp.name.lower()
            supp.save()
            return redirect("Supplier_list")
    params = {'form':form, 'error': error, 'error_statement': error_statement}
    return render(request, template_name, params)

def Supplier_update(request, pk, template_name='accounts/user_form.html'):
    user= get_object_or_404(Supplier, pk=pk)
    form = SupplierForm(request.POST or None,instance=user)
    if form.is_valid():
        supp=form.save(commit=False)
        supp.name = supp.name.lower()
        supp.save()
        return redirect('Supplier_list')
    return render(request, template_name, {'form':form})

def Supplier_delete(request, pk, template_name='accounts/user_confirm_delete.html'):
    user= get_object_or_404(Supplier, pk=pk)
    if request.method=='POST':
        user.delete()
        return redirect('Supplier_list')
    return render(request, template_name, {'object':user})

def homepage(request):
    print("entered homepage")
    uname = request.session['username']
    print("uname = "+uname)
    item_list = Item.objects.all()
    item=[]
    count=0
    for i in item_list:
        if i.total_no_of_units <= i.min_qty :
            item.append(i)
            count=count + 1
            if count ==5:
                break
    curr_date=datetime.date.today()
    new_date = curr_date + datetime.timedelta(days=5000)
    stock = Stock.objects.filter(exp_date__range=[curr_date,new_date])
    month=datetime.date.today().month
    if month in (4,6,9,11):
        days=30
    elif month == 2:
        days=28
    else:
        days=31
    a=curr_date + datetime.timedelta(days=(1-curr_date.day))
    print(a)
    new_date= a+datetime.timedelta(days=days)
    order=Order.objects.filter(date__range=[a,new_date])
    if stock.count() > 5:
        stock=stock[:5]

    order_total=0
    sales_total=0
    for i in order:
        order_total += i.gtotal
    sale=Invoice.objects.all()
    for i in sale:
        sales_total += i.gtotal
    print("sale "+ str(sales_total))
    print("order"+ str(order_total))
    monthly_list = Order.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('gtotal'))
    mon_sales_list=Invoice.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('gtotal'))
    return render(request,'accounts/admin_home_new.html',{'uname': uname,'item': item,
                                                          'stock': stock,'order_total':order_total,
                                                          'sales_total':sales_total,'monthly_list':monthly_list,
                                                         'mon_sales_list':mon_sales_list })
def worker_homepage(request,template_name='accounts/worker_home.html'):
    print("entered worker homepage")
    if request.session['username']=='':
        print("not authenticated")
    else:
        print("yes authen")
    uname = request.session['username']
    print("uname= "+request.session['username'])
    item_list = Item.objects.all()
    item = []
    count = 0
    for i in item_list:
        if i.total_no_of_units <= i.min_qty:
            item.append(i)
            count = count + 1
            if count == 5:
                break
    curr_date = datetime.date.today()
    new_date = curr_date + datetime.timedelta(days=5000)
    stock = Stock.objects.filter(exp_date__range=[curr_date, new_date])
    month = datetime.date.today().month
    if month in (4, 6, 9, 11):
        days = 30
    elif month == 2:
        days = 28
    else:
        days = 31
    a = curr_date + datetime.timedelta(days=(1 - curr_date.day))
    print(a)
    new_date = a + datetime.timedelta(days=days)
    order = Order.objects.filter(date__range=[a, new_date])
    if stock.count() > 5:
        stock = stock[:5]

    order_total = 0
    sales_total = 0
    for i in order:
        order_total += i.gtotal
    sale = Invoice.objects.all()
    for i in sale:
        sales_total += i.gtotal
    print("sale " + str(sales_total))
    print("order" + str(order_total))
    monthly_list = Order.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('gtotal'))
    mon_sales_list = Invoice.objects.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('gtotal'))
    return render(request, template_name, {'uname': uname, 'item': item,
                                                            'stock': stock, 'order_total': order_total,
                                                            'sales_total': sales_total,})


def Change_pwd(request,template_name='accounts/change_pwd.html'):
    uname=request.session['username']
    print(uname)
    error=False
    error_stat=''
    user=User.objects.get(username=uname)
    if request.method == "POST":
        curr_pwd=request.POST.get('curr_pwd')
        new_pwd=request.POST.get('new_pwd')
        confirm_pwd = request.POST.get('confirm_pwd')
        if user.password != curr_pwd:
            error=True
            error_stat= "Password Incorrect"
        else:
            if new_pwd != confirm_pwd :
                error=True
                error_stat=" new and confirm password doesn't match"
            else:
                user.password=new_pwd
                user.save()
                print("here saved changes")
                return redirect('homepage')
    params={'uname':uname,'error':error,'error_statement':error_stat}
    return render(request,template_name,params)

def Logout(request,template_name='accounts/logout.html'):
    print("in logout")
    if request.method == "POST":
        if request.POST.get("yes"):
            return redirect('index')
        if request.POST.get("no"):
            request.session['username'] =''
            print("uname set= "+ request.session['username'])
            return redirect('homepage')
    return render(request,template_name)