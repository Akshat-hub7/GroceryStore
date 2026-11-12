from django.contrib import admin
from .models import Products, Cart, Order

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'category', 'pub_date','offer_price', 'mrp', 'product_image')
    list_filter = ('category', 'pub_date')
    search_fields = ('product_name', 'category')
    radio_fields = {'category': admin.VERTICAL}  # Category as radio buttons

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'display_products')
    filter_horizontal = ('products',)  # Better UI for many-to-many field

    def display_products(self, obj):
        return ", ".join([p.product_name for p in obj.products.all()])
    display_products.short_description = "Products in Cart"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered_at', 'status', 'display_products')
    list_filter = ('status', 'ordered_at')
    search_fields = ('user__username', 'products__product_name')
    filter_horizontal = ('products',)

    def display_products(self, obj):
        return ", ".join([p.product_name for p in obj.products.all()])
    display_products.short_description = "Ordered Products"

# Register models with admin
admin.site.register(Products, ProductsAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
