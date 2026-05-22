from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    discount_percent = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100, blank=True, null=True, unique=True)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    supplier_name = models.CharField(max_length=150, blank=True)
    supplier_product_id = models.CharField(max_length=150, blank=True, null=True)
    external_image_url = models.URLField(blank=True, null=True)
    last_supplier_update = models.DateTimeField(blank=True, null=True)
    dimensions = models.CharField(max_length=200, blank=True)
    material = models.CharField(max_length=200, blank=True)
    fabric_type = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=100, blank=True)
    warranty = models.CharField(max_length=100, blank=True)
    delivery_time = models.CharField(max_length=100, blank=True)

    has_storage = models.BooleanField(default=False)

    features = models.TextField(blank=True)
    technical_details = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()

        if reviews.exists():
            return round(
                reviews.aggregate(models.Avg('rating'))['rating__avg'],
                1
            )

        return 0

    @property
    def discounted_price(self):
        if self.discount_percent > 0:
            discount_amount = self.price * self.discount_percent / 100
            return self.price - discount_amount

        return self.price
    
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.full_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=5)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'
    
class Favorite(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            unique_together = ('user', 'product')

        def __str__(self):
            return f'{self.user.username} - {self.product.name}'