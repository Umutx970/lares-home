from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Review, Favorite


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percent', 'is_new', 'is_featured', 'stock', 'is_active')
    list_editable = ('discount_percent', 'is_new', 'is_featured', 'stock', 'is_active')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Favorite)