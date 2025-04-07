from django.shortcuts import render

from catalog.models import Product, Category


def home(request):
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


def products(request, pk):
    # category_item = Category.objects.get(pk=pk)
    categories = Product.objects.filter(category_id=pk)
    context = {
        'object_list': categories
    }
    return render(request, 'catalog/products.html', context)
