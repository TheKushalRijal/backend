from rest_framework import serializers
from .models import Item, Product
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')  # Added username to the fields

    def validate_email(self, value):
        # Ensure email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value

    def create(self, validated_data):
        # Create a new user with the validated data
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])  # Ensure password is hashed
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

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
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'rating', 'inStock', 'store']  # Fields to include in JSON

    def to_representation(self, instance):
        data = super().to_representation(instance)  
        data['price'] = format(instance.price, '.2f') if instance.price is not None else None  # Ensure price has two decimal places
        return data
