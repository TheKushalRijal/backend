from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import base, ItemViewSet
from django.views.generic import TemplateView



router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    
    path('backend/', include(router.urls)),
    path('backend/location/', views.location, name='location'),
    path('',views.home, name='home'),
    path('tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('storesdata/', views.storesdata, name='storesdata'),  # Ensure it's POST request here

    path('backend/tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('read-excel/', views.read_excel_file, name='read_excel_file'),  # URL to trigger the Excel reading view
    path('import-excel/', views.import_excel_to_model, name='import_excel_to_model'),
    path('backend/nameitems/', views.items, name='items'),  # Updated the path to 'nameitems/'

    path('base/', views.base, name='base'),
    path('search/', views.serach, name='search'),
    path('gas/', views.gas, name='gas'),
    path('menu/', views.menu, name='menu'),
 
]
