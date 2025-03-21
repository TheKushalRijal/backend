from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User  # Django's built-in User model
#from views import userlocations


class Store(models.Model):
    address = models.CharField(max_length=255, null=True)  # Changed 'Address' to 'address' for consistency with naming conventions
    latitude = models.FloatField(default=0.0)  # Changed from CharField to FloatField for proper handling of latitude values
    longitude = models.FloatField(default=0.0)  # Changed from CharField to FloatField for proper handling of longitude values
    store_name = models.CharField(max_length=255, null=True)  # 'store_name' is more descriptive than just 'name'
    parkings = models.ImageField(null = True)

    def __str__(self):
        return self.store_name


class Item(models.Model):
    
    name = models.CharField(max_length=255,blank = True)  # Consider removing if title is enough
    title = models.CharField(max_length=255, null=True, blank=True)
    Store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)
    sku = models.CharField(max_length=50, null=True, unique=True)
    image = models.URLField(default="http://example.com/default-image.jpg") 
    in_stock = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.title or self.name} - {self.sku}"


class UserLocation(models.Model):
    location = models.CharField(max_length=255)  # User's location
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.CharField(max_length=30, default='0.0')
    longitude = models.CharField(max_length=30, default='0.0') # Use CharField for flexibility
    timestamp = models.DateTimeField(auto_now_add=True)  # Track when the location was saved

    def __str__(self):
        return f"{self.user.username} - {self.location}"
   



class ExcelFile(models.Model):
    file = models.FileField(upload_to='uploads/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)  # Link to Store model

    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    stock = models.IntegerField(null=True)
    inStock = models.CharField(null=True,blank=True,max_length=5)
    image = models.URLField(null=True,blank=True,default="http://example.com/default-image.jpg")  # Changed to URLField for online images
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],null = True)
    def __str__(self):
        return self.name
    
class finaltokens(models.Model):
    token = models.CharField(max_length=100)

