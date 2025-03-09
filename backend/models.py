from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Store(models.Model):
    api_key = models.CharField(max_length=255, unique=True)  # Unique API key per store
    location = models.CharField(max_length=255)
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name


class Item(models.Model):
    name = models.CharField(max_length=255,blank = True)  # Consider removing if title is enough
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    sku = models.CharField(max_length=50, null=True, unique=True)
    image = models.URLField(default="http://example.com/default-image.jpg") 
    in_stock = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.title or self.name} - {self.sku}"


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)  # Track which user saved this location
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.location}"
    
class Token(models.Model):  # Renaming the class to Token
    usertokens = models.CharField(null=False, max_length=100)


class ExcelFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # 'uploads/' will store the file in MEDIA_ROOT/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    stock = models.IntegerField(null=True)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],null = True)
    def __str__(self):
        return self.name