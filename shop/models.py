from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils import timezone
#


class Category(models.Model):
    """Category model"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Kategoriya")
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

FILTER_CHOICES = {
    'po': 'Popularity',
    'org': 'Organic',
    'fan': 'Fantastic'
}

class Product(models.Model):
    """Product model"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    filter_choice = models.CharField(max_length=3, choices=FILTER_CHOICES, null=True)
    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', verbose_name="Rasmi")
    slug = models.SlugField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Rating(models.Model):
    """Rating model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name}: {self.rating}"


class Customer(models.Model):
    """Customer model"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100,null=True, default='')
    last_name = models.CharField(max_length=100, null=True, default='')


class Order(models.Model):
    """Order model"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    @property
    def get_cart_total_price(self):
        order_product = self.orderproduct_set.all()
        total_price = sum([product.get_cart_price for product in order_product])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_product = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_product])
        return total_quantity

class OrderProduct(models.Model):
    """OrderProduct model"""
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)


    @property
    def get_cart_price(self):
        total_price =self.quantity * self.product.price
        return total_price


class ShippingAddress(models.Model):
    """ShippingAddress model"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)
    mobile = models.CharField(max_length=13)
    email = models.EmailField(max_length=100)

class CustomerMessage(models.Model):
    """CustomerMessage model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)