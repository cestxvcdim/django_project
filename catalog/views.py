from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, Category


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/home.html'


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.filter(category_id=self.kwargs['pk'])
        return context


class ProductDetailView(DetailView):
    model = Product


"""
Возникает ошибка ValueError: The view catalog.views.view didn't return an HttpResponse object. It returned None instead.
При этом данные от принта в консоль выводятся, как исправить?

class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f'name: {name}\nphone: {phone}\nmessage: {message}')
            return
        else:
            return render(request, 'catalog/contacts.html')
"""


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}\nphone: {phone}\nmessage: {message}')
    return render(request, 'catalog/contacts.html')
