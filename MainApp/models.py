from django.db import models
from django.conf import settings


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField()
    offer_price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='products/')
    pub_date = models.DateField()
    
    CATEGORY_CHOICES = [
        ('dairy', 'Dairy'),
        ('fruits', 'Fruits'),
        ('vegetables', 'Vegetables'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('bakery', 'Bakery'),
        ('meat', 'Meat'),
        ('seafood', 'Seafood'),
        ('frozen', 'Frozen Foods'),
        ('grains', 'Grains & Cereals'),
        ('personal_care', 'Personal Care'),
        ('cleaning', 'Cleaning Supplies'),
        ('stationery', 'Stationery'),
        ('baby_products', 'Baby Products'),
        ('health', 'Health & Wellness'),
        ('pet_supplies', 'Pet Supplies'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.product_name


from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Products, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Products)
    ordered_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"
