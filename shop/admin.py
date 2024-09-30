from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart'] 
 
 
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['created_at' , 'updated_at'] 
    
    
