from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, ShippingAddress, Customer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_image')
    list_display_link = ('id', 'name')

    def get_image(self, category):
        return mark_safe(f'<img src="{category.image.url}" width="50" height="50" />')
    
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount', 'quantity', 'category', 'get_image')
    list_display_links = ('id', 'name')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px;">')
        return '-'

    get_image.short_description = 'Rasmi'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name')
    list_display_links = ('id', 'user')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'address', 'district', 'zip_code', 'email', 'mobile')
    list_display_links = ('id', 'city')
