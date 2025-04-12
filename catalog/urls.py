from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('categories/<int:pk>/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/create', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product_delete'),
    path('version/<int:pk>/', views.VersionDetailView.as_view(), name='version_detail'),
    path('version/create', views.VersionCreateView.as_view(), name='version_create'),
    path('version/<int:pk>/update', views.VersionUpdateView.as_view(), name='version_update'),
]