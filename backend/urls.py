from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet,location,tokens,items,nearbylocations,page,import_excel_to_model # Ensure views is imported correctly
from . import views



router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    
    path('backend/', include(router.urls)),
    path('backend/location/', views.location, name='location'),
    path('',views.page,name='locations'),
    path('nearbylocations/', nearbylocations, name='nearbylocations'),  # Nearby locations API



    path('tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('storesdata/', views.storesdata, name='storesdata'),  # Ensure it's POST request here

    path('backend/tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('read-excel/', views.read_excel_file, name='read_excel_file'),  # URL to trigger the Excel reading view
    path('import-excel/', views.import_excel_to_model, name='import_excel_to_model'),
    path('backend/nameitems/', views.items, name='items'),  # Updated the path to 'nameitems/'


]
