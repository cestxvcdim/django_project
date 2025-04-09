from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('<int:pk>/categories/', views.product_list, name='product_list'),
    path('<int:pk>/products/', views.product_detail, name='product_detail'),
]