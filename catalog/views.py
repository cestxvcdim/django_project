from django.shortcuts import render

from catalog.models import Product, Category


def home(request):
    """Categories list"""

    categories = Category.objects.all()
    context = {
        'object_list': categories
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}\nphone: {phone}\nmessage: {message}')
    return render(request, 'catalog/contacts.html')


def product_list(request, pk):
    """Products list"""

    # category_item = Category.objects.get(pk=pk)
    products = Product.objects.filter(category_id=pk)
    context = {
        'object_list': products
    }
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, pk):
    """Product details"""

    product_item = Product.objects.get(pk=pk)
    context = {
        'product': product_item
    }
    return render(request, 'catalog/product_detail.html', context)