from django.contrib import admin
from .models import Item, Store# Import your models

admin.site.register(Item)
admin.site.register(Store)
