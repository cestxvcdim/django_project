from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Category, Version

from catalog.services import get_cached_category_list, get_cached_product_info


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = get_cached_category_list()
        return context


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.filter(category_id=self.kwargs['pk'])
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_info = get_cached_product_info(kwargs['object'].pk)
        context['product_name'] = product_info['name']
        context['product_category'] = product_info['category']
        context['product_created_at'] = product_info['created_at']
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product

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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm

        if user.groups.filter(name="Moderator").exists():
            return ProductModeratorForm

        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
    permission_required = 'catalog.delete_product'
    context_object_name = 'product'

    def test_func(self):
        return self.request.user.is_superuser


class VersionDetailView(LoginRequiredMixin, DetailView):
    model = Version

    def get_object(self, queryset=None):
        version = Version.objects.get(product=self.kwargs['pk'], is_actual=True)
        return version


class VersionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.add_version'
    success_url = reverse_lazy('catalog:home')


class VersionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    permission_required = 'catalog.change_version'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        version = Version.objects.get(product=self.kwargs['pk'], is_actual=True)
        version.is_actual = False
        version.save()

        self.object = super().get_object(queryset)
        self.object.is_actual = True
        self.object.save()
        return self.object


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'name: {name}\nphone: {phone}\nmessage: {message}')
    return render(request, 'catalog/contacts.html')
