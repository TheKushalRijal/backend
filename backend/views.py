from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Item, UserLocation, Product,finaltokens,Store
from .serializers import ItemSerializer, ProductSerializer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
import pandas as pd
import os
from django.conf import settings
from django.contrib.auth.models import User
import math


# ItemViewSet remains unchanged
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()  # Define the queryset explicitly
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        
        # Apply filters based on query parameters
        query = self.request.query_params.get('query', '')
        in_stock = self.request.query_params.get('inStock', None)
        min_price = self.request.query_params.get('minPrice', None)
        max_price = self.request.query_params.get('maxPrice', None)
        sort = self.request.query_params.get('sort', None)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |  # Ensure correct field name
                Q(description__icontains=query) | 
                Q(sku__icontains=query)
            )

        if in_stock is not None:
            in_stock = in_stock.lower() == 'true'
            queryset = queryset.filter(in_stock=in_stock)

        if min_price is not None:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                return Response({"error": "Invalid minPrice value"}, status=400)

        if max_price is not None:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                return Response({"error": "Invalid maxPrice value"}, status=400)

        valid_sorts = {
            "price-asc": "price",
            "price-desc": "-price",
            "rating": "-rating",
            "name": "name"
        }

        if sort in valid_sorts:
            queryset = queryset.order_by(valid_sorts[sort])

        return queryset


# Updated tokens view to handle both location and token
@api_view(['POST'])
def location(request):
    location = request.data.get('location', None)
    postal_code = request.data.get('postal_code', None)
    longitude = request.data.get("longitude",None)
    latitude = request.data.get("latitude",None)
    if not location or not postal_code:
        return Response({"error": "Location and postal code are required"}, status=400)
    
    try:
        # Assuming the user is authenticated and available in the request
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=401)
        
        # Save the location to the UserLocation model
        user_location = UserLocation.objects.create(
            user=user.username,  # Store the username (or use user.id)
            location=location,
            postal_code=postal_code,
        )
        
        return Response({
            "message": "Location saved successfully",
            "location": location,
            "postal_code": postal_code
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# View to save user token
@api_view(['POST'])
def tokens(request):
    token = request.data.get('token', None)
    print(token)
    if not token:
        return Response({"error": "Token is required"}, status=400)

    try:
        # Save the token to the UserLocation model
        user_location = finaltokens.objects.create(token=token)
        
        return Response({
            "message": "Token saved successfully",
            "token": token,
        })
    except Exception as e:
        return Response({"errojdagf avgsdfr": str(e)}, status=100)



# View to search for products by name
@api_view(['GET'])
def productname(request):
    name = request.GET.get("item_name", None)  # Retrieve item_name from GET request

    if not name:
        return Response({"error": "Item name is required"}, status=400)

    items = Product.objects.filter(name__iexact=name)  # Case-insensitive match

    if not items.exists():
        return Response({"error": "Item not found"}, status=404)

    serializer = ProductSerializer(items, many=True)  # Support multiple matches
    return Response(serializer.data)


# View to list items with optional sorting and filtering
@api_view(['GET'])
def items(request):
    name = request.GET.get("query", "").strip()  # Get search query
    sort = request.GET.get("sort", None)  # Get sort parameter

    # Filter items based on query (case-insensitive search)
    if name:
        items = Product.objects.filter(name__icontains=name)
    else:
        return Response([], status=200)  # Return empty list if no query is provided

    # Apply sorting only if sort is provided
    valid_sort_fields = ["name", "-name", "price", "-price", "created_at", "-created_at"]
    if sort and sort in valid_sort_fields:
        items = items.order_by(sort)

    # Serialize and return results
    serializer = ProductSerializer(items, many=True)
    return Response(serializer.data, status=200)


# View to read an Excel file and return its data as JSON
def read_excel_file(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'backend', 'static', 'excel_files', 'your_file.xlsx')
    
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        data = df.to_dict(orient="records")
        return JsonResponse({"data": data})
    except Exception as e:
        return JsonResponse({"error": str(e)})


# View to import data from an Excel file into the Product model
def import_excel_to_model(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'backend', 'static', 'excel_files', 'datafile.xlsx')

    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        
        for _, row in df.iterrows():
            Product.objects.create(
                name=row['Name'],
                description=row['Description'],
                price=row['Price'],
                stock=row['Stock'],
            )
        
        return JsonResponse({"message": "Data imported successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    


def nearbylocations(latitude, longitude, radius_m):
    stores = Store.objects.all()  # Assuming your store model is named `Store`
    nearby_stores = []
    
    for store in stores:
        distance = haversine(latitude, longitude, store.latitude, store.longitude)
        if distance <= radius_m:
            nearby_stores.append({
                'store': store,
                'distance': distance
            })
    
    nearby_stores.sort(key=lambda x: x['distance'])  # Sorting stores by distance
    return nearby_stores

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = R * c  # Distance in kilometers
    return distance_km * 1000  # Convert to meters


def storesdata(request):
    excel_file_path = os.path.join(settings.BASE_DIR, 'backend', 'static', 'excel_files', 'fileforstores.xlsx')
    
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        
        # Iterate through each row in the DataFrame
        for _, row in df.iterrows():
            # Create a new Store instance with the correct field names
            Store.objects.create(
                store_name=row['Name'],   # Correct field name is 'store_name'
                address=row['Address'],   # Correct field name is 'address'
                latitude=row['Latitude'], # Latitude as is
                longitude=row['Longitude']# Longitude as is
            )
        
        return JsonResponse({"message": "Data imported successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def name(request):
    # Query all Store objects
    stores = Store.objects.all()
    
    # Extract the store_name from each store and store it in a list
    store_names = [store.store_name for store in stores]
    
    # Print the store names to the console (for debugging purposes)
    print(store_names)
    
    # Return the store names as an HTTP response (or as a string)
    return HttpResponse(", ".join(store_names))