from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OderFilter
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.
# def home(request):
#     orders = Order.objects.all()
#     customers = Customer.objects.all()
#     context = {'orders': 'orders', 'customers':'customers'}
   
#     return render(request, 'accounts/dashboard.html', context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:     
        form = CreateUserForm()
        context = {'form': form}

        if request.method =='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')

                messages.success(request, 'Account was created for ' + user)

                return redirect('login')


    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:   

        if request.method == 'POST':
            username =request.POST.get('username')
            password = request.POST.get('password') 
            

            user = authenticate(request, username = username, password=password )
        
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')

    form = CreateUserForm()
    context ={'form': form}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout (request)
    return redirect('login')

@login_required(login_url='login')
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    #out_of_delivery = orders.filter(status  = 'Out for delivery ').count()

    context = {'orders': orders, 'customers': customers,
               'total_customers': total_customers,
               'total_orders': total_orders, 
               'delivered': delivered,
                'pending': pending }

    

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def userPage(request):
    context ={}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()    
    return render (request, 'accounts/products.html',{'products':products})
    #return render(request, 'accounts/products.html')


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders =customer.order_set.all() #child from models
    orders_count = orders.count()

    myFilter = OderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,'orders': orders, 'orders_count': orders_count, 'myFilter':myFilter}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
def createOrder(request, pk):
    customer = Customer.objects.get(id=pk)

#variable name
    OrderFormSet = inlineformset_factory(Customer, Order , fields=('product', 'status'), extra = 10)#(parentmodel, child model,instance  )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    #form = OrderForm(initial= {'customer': customer}) #mdoels bata ra  mathi create abta 
    if request.method == 'POST':
        # print('Printing POST:',request.POST )
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
              
    context = {'formset': formset}

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing POST:',request.POST )
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')


    context = {'form': form}
    return render(request,'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context={'item':order}

    return render(request, 'accounts/delete.html', context)