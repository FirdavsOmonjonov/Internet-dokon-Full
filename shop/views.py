from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .utils import CartAuthenticationUser
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from shop import models
import stripe
from django.contrib.auth.models import User
from . import models




def index(request):
    """Home page"""
    categories = models.Category.objects.all()
    cart_info = CartAuthenticationUser(request).get_cart_info() 
    products = models.Product.objects.all()
    new_products = models.Product.objects.all()[::-1]
    
    context = {
        'categories': categories,
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'products': products,
        'new_products': new_products,
        
    }

    return render(request, 'shop/all_products.html', context)



def shop(request):
    """Shop page"""
    cart_info = CartAuthenticationUser(request).get_cart_info() 
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    new_products = models.Product.objects.all()[::-1]
    
    context = {
        'categories': categories,
        'products': products,
        'new_products': new_products,
        'page_name': "Shop",
        'cart_total_quantity': cart_info['cart_total_quantity'],
        
    }
    return render(request, 'shop/shop.html', context)

def sorting(request: HttpRequest, key_name) -> HttpResponse:
    """Sorting products view at func level"""
    context = {
        'products': models.Product.objects.filter(filter_choice=key_name),
        
    }
    return render(request, 'shop/shop.html', context)


def filter_products_by_price(request):
    """Sorting products view at func level"""
    if request.method == 'POST':
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        if min_price:
            min_price = float(min_price)
        else:
            min_price = 0.0
        if max_price:
            max_price = float(max_price)
        else:
            max_price = 250.0
        products = models.Product.objects.filter(price__range=(min_price, max_price))
    else:
        products = models.Product.objects.all()
    context = {
        'products': products,
    }

    return render(request, 'shop/shop.html', context)


def product_detail(request, id):
    """Product detail page"""
    categories = models.Category.objects.all()
    product = models.Product.objects.get(id=id)
    products = models.Product.objects.filter(category=product.category)
    messages = models.CustomerMessage.objects.filter(product=product)[::-1]
    context = {
        'categories': categories,
        'product': product,
        'products': products,
        'messages': messages,
        'page_name': "Detail",
        
    }
    return render(request, 'shop/detail.html', context)


@login_required(login_url='login')
def cart(request):
    """Cart page"""
    new_products = models.Product.objects.all()[::-1]
    cart_info = CartAuthenticationUser(request).get_cart_info() 
    context = {
        'order_products': cart_info['order_products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'new_products': new_products,
        'page_name': "Cart",
    }

    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def to_cart(request:HttpRequest, product_id, action):
    """Add or remove product from cart"""
    CartAuthenticationUser(request, product_id, action)
    current_page = request.META.get('HTTP_REFERER', 'home')
    return redirect(current_page)
    

@login_required(login_url='login')
def clear_cart(request):
    """Clear cart"""
    cart_info = CartAuthenticationUser(request).get_cart_info()
    order = cart_info['order']
    order_products = order.orderproduct_set.all()
    for order_product in order_products:
        product = order_product.product
        product.quantity += order_product.quantity
        product.save()
        order_product.delete()
    return redirect('cart')
    

def checkout(request):
    cart_info = CartAuthenticationUser(request).get_cart_info() 
    context = {
        'order_products': cart_info['order_products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'page_name': "Checkout",
    }
    return render(request, 'shop/checkout.html', context)


def shipping_address(request):
    """Shipping address page"""
    if request.method == 'POST':
        models.Customer.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
        )
        models.ShippingAddress.objects.create(
            mobile=request.POST.get('mobile'),
            zip_code=request.POST.get('zip_code'),
            address=request.POST.get('address'),
            district=request.POST.get('district'),
            city=request.POST.get('city'),
            email=request.POST.get('email')
        )
        return redirect('checkout')  # Assuming 'checkout' is the name of the URL pattern
    return render(request, 'shop/checkout.html')


def customer_message(request):
    """Customer message page"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        customer_id = request.POST.get('customer_id')
        
        try:
            product =  models.Product.objects.get(id=product_id)
            customer =  models.Customer.objects.get(id=customer_id) if customer_id else None
            
            models.CustomerMessage.objects.create(
                product=product,
                customer=customer,
                message=request.POST.get('message'),
            )
            return redirect('detail', id=product.id)
        except Product.DoesNotExist:
          
            return redirect('shop')  
    return render(request, 'shop/detail.html')


def create_checkout_sessions(request):
    """Create checkout session"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticationUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online Shop mahsulotlari'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)


def success_payment(request):
    """Success page"""
    return render(request, 'shop/success.html')


def log_in(request):
    """Log in to"""
    context = {
        'page_name': "Login/Register",
    }
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
        except:
            return redirect('login')
    return render(request, 'auth/login.html', context)


def register(request):
    """Register to"""
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            print(username)
            print(password)
            print(confirm_password)
            if password == confirm_password:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
        except:
            return redirect('register')
    return render(request, 'auth/register.html')


def log_out(request):
    """Log out of"""
    logout(request)
    context = {
        'page_name': "Error",
    }
    return redirect('error')


def error(request):
    """Login error"""
    context = {
        'page_name': "Error",
    }
    return render(request, 'auth/error2.html', context)


def profile(request):
    """Profile page"""
    shipping_address = models.ShippingAddress.objects.all()
    cart_info = CartAuthenticationUser(request).get_cart_info() 
    context = {
        'order_products': cart_info['order_products'],
        'cart_total_price': cart_info['cart_total_price'],
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'page_name': "My account",
    }
    return render(request, 'auth/my_acount.html', context)



