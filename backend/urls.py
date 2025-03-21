from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
=======
from .views import ItemViewSet,location,tokens,items,nearbylocations,page,import_excel_to_model # Ensure views is imported correctly
>>>>>>> main
from . import views
from .views import base, ItemViewSet
from django.views.generic import TemplateView



router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    
    path('backend/', include(router.urls)),
    path('backend/location/', views.location, name='location'),
<<<<<<< HEAD
    path('',views.home, name='home'),
=======
    path('',views.page,name='locations'),
    path('nearbylocations/', nearbylocations, name='nearbylocations'),  # Nearby locations API



>>>>>>> main
    path('tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('storesdata/', views.storesdata, name='storesdata'),  # Ensure it's POST request here

    path('backend/tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('read-excel/', views.read_excel_file, name='read_excel_file'),  # URL to trigger the Excel reading view
    path('import-excel/', views.import_excel_to_model, name='import_excel_to_model'),
    path('backend/nameitems/', views.items, name='items'),  # Updated the path to 'nameitems/'

<<<<<<< HEAD
    path('base/', views.base, name='base'),
    path('search/', views.serach, name='search'),
    path('gas/', views.gas, name='gas'),
    path('menu/', views.menu, name='menu'),
 
=======

>>>>>>> main
]
