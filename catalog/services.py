from django.core.cache import cache

from config import settings
from catalog.models import Product, Category


def get_cached_products_by_category(category_id: int):
    if settings.CACHE_ENABLED:
        key = f'category_list_{category_id}'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Product.objects.filter(category_id=category_id)
            cache.set(key, category_list)
    else:
        category_list = Product.objects.filter(category_id=category_id)
    return category_list


def get_cached_category_list():
    if settings.CACHE_ENABLED:
        key = f'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list


def get_cached_product_info(product_id: int):
    if settings.CACHE_ENABLED:
        key = f'product_info_{product_id}'
        product_info = cache.get(key)
        if product_info is None:
            product = Product.objects.get(pk=product_id)
            name = product.name
            category = product.category
            created_at = product.created_at
            product_info = {
                'name': name,
                'category': category,
                'created_at': created_at,
            }
            cache.set(key, product_info)
    else:
        product = Product.objects.get(pk=product_id)
        name = product.name
        category = product.category
        created_at = product.created_at
        product_info = {
            'name': name,
            'category': category,
            'created_at': created_at,
        }

    return product_info
