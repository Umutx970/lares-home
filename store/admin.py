from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'brand',
        'category',
        'price',
        'stock',
        'supplier_name',
        'is_active',
    )

    search_fields = (
        'name',
        'brand',
        'sku',
        'barcode',
    )

    list_filter = (
        'category',
        'brand',
        'is_active',
    )


admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Favorite)