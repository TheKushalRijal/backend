from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, userlocations ,page,tokens,items # Ensure views is imported correctly
from . import views



router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    
    path('backend/', include(router.urls)),
    path('location', userlocations, name='user-Locations'),
   # path('',userlocations,name='user-Locations'),
    path('',page,name='mypage'),
    path('tokens/', views.tokens, name='tokens'),  # Ensure it's POST request here
    path('read-excel/', views.read_excel_file, name='read_excel_file'),  # URL to trigger the Excel reading view
    path('import-excel/', views.import_excel_to_model, name='import_excel_to_model'),
    path('backend/nameitems/', views.items, name='items'),  # Updated the path to 'nameitems/'



]
