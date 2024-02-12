from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from forms import OrderForm



# Create your views here.
# def home(request):
#     orders = Order.objects.all()
#     customers = Customer.objects.all()
#     context = {'orders': 'orders', 'customers':'customers'}
   
#     return render(request, 'accounts/dashboard.html', context)

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

    context = {'customer': customer,'orders': orders, 'orders_count': orders_count}
    return render(request, 'accounts/customers.html', context)

def createOrder(request):

    context = {}

    return render(request, 'accounts/order_form.html', context)