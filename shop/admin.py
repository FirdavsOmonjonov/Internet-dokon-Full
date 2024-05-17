from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_image')
    list_display_link = ('id', 'name')

    def get_image(sels, category):
        return mark_safe(f'<img src="{category.image.url}" width="50" height="50" />')
    
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount', 'weight', 'category', 'get_image')
    list_display_links = ('id', 'name')

    def get_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="75px;">')
        return '-'

    get_image.short_description = 'Rasmi'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id',  'rating')
    list_display_links = ('id', 'rating')