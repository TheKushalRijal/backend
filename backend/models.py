from django.db import models
from django.contrib.auth.models import User  # Django's built-in User model



class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Store", null = True)

    api_key = models.CharField(max_length=255, unique=True)  # Unique API key per store
    location = models.CharField(max_length=255)
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name


class Item(models.Model):
    Store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255,null=True)
    description = models.TextField()
    price = models.DecimalField(null = True,max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, null=True)
    image = models.URLField(default="http://example.com/default-image.jpg") 
    in_stock = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    stock_count = models.DecimalField(null=True, max_digits=500, decimal_places=2)

    def __str__(self):
        return f"{self.title} - {self.sku}"