from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Item
from .serializers import ItemSerializer
from django.db.models import Q



class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()  # Define the queryset explicitly
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        
        # Apply filters based on query parameters (same logic as before)
        query = self.request.query_params.get('query', '')
        in_stock = self.request.query_params.get('inStock', None)
        min_price = self.request.query_params.get('minPrice', None)
        max_price = self.request.query_params.get('maxPrice', None)
        sort = self.request.query_params.get('sort', None)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(sku__icontains=query)
            )

      
        if in_stock is not None:
            in_stock = in_stock.lower() == 'true'
            queryset = queryset.filter(in_stock=in_stock)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        if sort:
            if sort == 'price-asc':
                queryset = queryset.order_by('price')
            elif sort == 'price-desc':
                queryset = queryset.order_by('-price')
            elif sort == 'rating':
                queryset = queryset.order_by('-rating')
            elif sort == 'name':
                queryset = queryset.order_by('title')

        return queryset
