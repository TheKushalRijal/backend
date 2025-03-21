from rest_framework import serializers
from .models import Item,Product

class ItemSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(min_value=0.0, max_value=5.0)  # Ensures valid ratings
    price = serializers.DecimalField(max_digits=10, decimal_places=2)  # Ensures correct decimal format

    class Meta:
        model = Item
        fields = ['id', 'name', 'title', 'description', 'price', 'sku', 'image', 'in_stock', 'rating']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = format(instance.price, '.2f')  # Format price as string with 2 decimal places
        return data


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(min_value=0.0, max_value=5.0, required=False, allow_null=True)  
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)  

    class Meta:
        model = Product  # Specifies that this serializer is for the Product model
        fields = ['id', 'name', 'description', 'price', 'stock','image', 'rating','inStock','store']  # Fields to include in JSON

    def to_representation(self, instance):
        data = super().to_representation(instance)  
        data['price'] = format(instance.price, '.2f') if instance.price is not None else None  # Ensure price has two decimal places
        return data