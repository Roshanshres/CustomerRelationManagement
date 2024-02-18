from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OderFilter
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# def home(request):
#     orders = Order.objects.all()
#     customers = Customer.objects.all()
#     context = {'orders': 'orders', 'customers':'customers'}
   
#     return render(request, 'accounts/dashboard.html', context)

def registerPage(request):
    form = CreateUserForm()
    context = {'form': form}

    if request.method =='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()


    return render(request, 'accounts/register.html', context)


def loginPage(request):

    form = CreateUserForm()
    context ={'form': form}
    return render(request, 'accounts/login.html', context)

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


def products(request):
    products = Product.objects.all()    
    return render (request, 'accounts/products.html',{'products':products})
    #return render(request, 'accounts/products.html')

def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders =customer.order_set.all() #child from models
    orders_count = orders.count()

    myFilter = OderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,'orders': orders, 'orders_count': orders_count, 'myFilter':myFilter}
    return render(request, 'accounts/customers.html', context)

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

def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context={'item':order}

    return render(request, 'accounts/delete.html', context)