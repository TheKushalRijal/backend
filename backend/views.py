from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from .models import Item, UserLocation, Token,Product
from .serializers import ItemSerializer,ProductSerializer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,get_object_or_404
import pandas as pd
import os
from django.conf import settings



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



#@api_view(['POST'])
def userlocations(request):
    # Get location and address from request body
    userAddress = request.data.get("userAddress", None)
    userPostalCode = request.data.get("userPostalCode", None)

    if not userAddress or not userPostalCode:
        return Response({"error": "Address and Postal Code are required"}, status=400)

    # Save location to the database
    user_location = UserLocation.objects.create(
        location=userAddress,
        postal_code=userPostalCode
    )
    
    return Response({"message": "Location saved successfully", "location": user_location.location})




def page(request):
    return render(request,"index.html")




#@api_view(['GET'])
def itemname(request):
    item_name = request.GET.get("item_name", None)  # Retrieve item_name from GET request

    if not item_name:
        return Response({"error": "Item name is required"}, status=400)

    items = Product.objects.filter(name__iexact=item_name)  # Case-insensitive match

    if not items.exists():
        return Response({"error": "Item not found"}, status=404)

    serializer = ItemSerializer(items, many=True)  # Support multiple matches
    return Response(serializer.data)  # Return serialized data as JSON



'''
@api_view(["POST"])  # Change this to POST if you want to accept POST requests
def tokens(request):
    token_value = request.data.get("token", None)  # Get token from POST body

    if not token_value:
        return Response({"error": "Tokens not provided"}, status=400)

    # Assuming 'tokens' is the model where tokens are stored
    user_token = get_object_or_404(Token, usertokens=token_value)

    return Response({"user_tokens": user_token.usertokens}, status=200)'
    '''
@api_view(['GET'])
def tokens(request):
    token = request.data.get('token')
    print(token)  # Debugging

    return Response({"message": "Token processed successfully"})


def read_excel_file(request):
    # Define the path to your manually added Excel file
    excel_file_path = os.path.join(settings.BASE_DIR, 'backend', 'static', 'excel_files', 'your_file.xlsx')
    
    try:
        # Read the Excel file using pandas
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        
        # Convert the DataFrame to JSON format (as a list of records)
        data = df.to_dict(orient="records")
        
        return JsonResponse({"data": data})  # Send the data as JSON response
    except Exception as e:
        return JsonResponse({"error": str(e)})
    

def import_excel_to_model(request):
    # Path to the manually added Excel file in your static folder
    excel_file_path = os.path.join(settings.BASE_DIR, 'backend', 'static', 'excel_files', 'datafile.xlsx')

    try:
        # Read the Excel file using pandas
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        
        # Iterate through the rows of the DataFrame and save to the model
        for _, row in df.iterrows():
            # Create and save a new Product instance for each row
            Product.objects.create(
                name=row['Name'],           # Assuming the column in the Excel file is 'Name'
                description=row['Description'],  # Assuming the column in the Excel file is 'Description'
                price=row['Price'],         # Assuming the column in the Excel file is 'Price'
                stock=row['Stock'],         # Assuming the column in the Excel file is 'Stock'
            )
        
        return JsonResponse({"message": "Data imported successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    
def productname(request):
    name = request.GET.get("item_name", None)  # Retrieve item_name from GET request

    if not name:
        return Response({"error": "Item name is required"}, status=400)

    items = Product.objects.filter(name__iexact=name)  # Case-insensitive match

    if not items.exists():
        return Response({"error": "Item not found"}, status=404)

    serializer = ProductSerializer(items, many=True)  # Support multiple matches
    return Response(serializer.data)
@api_view(['GET'])
def items(request):
    name = request.GET.get("query", "").strip()  # Get search query
    sort = request.GET.get("sort", None)  # Get sort parameter

    print(f"Received query: {name}")  # Debugging print

    # Filter items based on query (case-insensitive search)
    if name:
        items = Product.objects.filter(name__icontains=name)
    else:
        return Response([], status=200)  # Return empty list if no query is provided

    print(f"Filtered items: {items}")  # Debugging print

    # Apply sorting only if sort is provided
    valid_sort_fields = ["name", "-name", "price", "-price", "created_at", "-created_at"]
    if sort and sort in valid_sort_fields:
        items = items.order_by(sort)

    # Serialize and return results
    serializer = ProductSerializer(items, many=True)
    return Response(serializer.data, status=200)
