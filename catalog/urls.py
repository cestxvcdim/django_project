from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('<int:pk>/categories/', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/products/', views.ProductDetailView.as_view(), name='product_detail'),
]