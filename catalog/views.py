from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Category, Version


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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        ProductFormset = inlineformset_factory(Product, Version, form=ProductForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = ProductFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save(commit=False)

        if formset.is_valid():
            formset.instance = self.object
            formset.instance.updated_at = timezone.now()
            formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs['pk']])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    context_object_name = 'product'


class VersionDetailView(DetailView):
    model = Version


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:home')


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:home')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}\nphone: {phone}\nmessage: {message}')
    return render(request, 'catalog/contacts.html')
