from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .utils import CartAuthenticationUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from shop import models
from django.contrib.auth.models import User





def index(request):
    """Home page"""
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    new_products = models.Product.objects.all()[::-1]
    
    context = {
        'categories': categories,
        'products': products,
        'new_products': new_products,
        
    }

    return render(request, 'shop/all_products.html', context)



def shop(request):
    """Shop page"""
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    new_products = models.Product.objects.all()[::-1]
    
    context = {
        'categories': categories,
        'products': products,
        'new_products': new_products,
        'page_name': "Shop",
        
    }
    return render(request, 'shop/shop.html', context)

def sorting(request: HttpRequest, key_name) -> HttpResponse:
    """Sorting products view at func level"""
    context = {
        'products': models.Product.objects.filter(filter_choice=key_name),
        
    }
    return render(request, 'shop/shop.html', context)

def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = models.Product.objects.get(id=product_id)
    models.Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return redirect('detail', id = product.id)


def filter_products_by_price(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        # Filter products where price is between min_price and max_price
        products = models.Product.objects.filter(price__range=(min_price, max_price))
    elif min_price:
        # Filter products where price is greater than or equal to min_price
        products = models.Product.objects.filter(price__gte=min_price)
    elif max_price:
        # Filter products where price is less than or equal to max_price
        products = models.Product.objects.filter(price__lte=max_price)
    else:
        # If no price range is specified, return all products
        products = models.Product.objects.all()

    return render(request, 'shop/shop.html', {'products': products})




def product_detail(request, id):
    """Product detail page"""
    categories = models.Category.objects.all()
    product = models.Product.objects.get(id=id)
    products = models.Product.objects.filter(category=product.category)

    context = {
        'categories': categories,
        'product': product,
        'products': products,
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
    return render(request, 'shop/checkout.html')



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
                return render(request,'auth/error.html')
        except:
            return redirect('error')
        
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
    return redirect('error2')


def error(request):
    """Login error"""
    context = {
        'page_name': "Error",
    }
    return render(request, 'auth/error.html', context)

def error2(request):
    """Login error"""
    context = {
        'page_name': "Error",
    }
    return render(request, 'auth/error2.html', context)

def profile(request):
    """Profile page"""
    context = {
            'page_name': "My account",
        }
    return render(request, 'auth/my_acount.html', context)



