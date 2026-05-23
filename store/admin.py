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

    list_editable = (
        'stock',
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
        'has_storage',
    )

    fieldsets = (
        ('Temel Bilgiler', {
            'fields': (
                'category',
                'name',
                'brand',
                'price',
                'description',
                'image',
                'external_image_url',
                'stock',
                'is_active',
            )
        }),
        ('Tedarikçi Bilgileri', {
            'fields': (
                'sku',
                'barcode',
                'supplier_name',
                'supplier_product_id',
                'last_supplier_update',
            )
        }),
        ('Mobilya / Ürün Detayları', {
            'fields': (
                'dimensions',
                'material',
                'fabric_type',
                'color',
                'warranty',
                'delivery_time',
                'has_storage',
                'features',
                'technical_details',
            )
        }),
        ('Etiketler', {
            'fields': (
                'is_featured',
                'is_new',
                'discount_percent',
            )
        }),
    )

admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Favorite)