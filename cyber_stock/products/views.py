# from django.template import RequestContext
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .models import *
from .forms import *

class ListProductTypes(ListView):
    model = ProductType

    def get_queryset(self):
        product_types = ProductType.objects.all()

        queryset = []

        for product_type in product_types:
            products = Product.objects.filter(product_type=product_type)
            queryset.append({
                'product_type': product_type, 
                'products_qtd': len(products)
            })

        return queryset



class CreateProductType(CreateView):
    model = ProductType
    fields = [
        'name',
        'description'
    ]
    success_url = reverse_lazy('product_types')


class ListProducts(ListView):
    model = Product

    def get_queryset(self):
        product_type = ProductType.objects.get(pk=self.kwargs['id'])
        products = Product.objects.filter(product_type=product_type)
        return products
        

class CreateProduct(CreateView):
    model = Product
    form_class = CreateProductForm
    success_url = reverse_lazy('product_types')


class UpdateProductType(UpdateView):
    model = ProductType
    fields = [
        'name',
        'description'
    ]
    success_url = reverse_lazy('product_types')
    
class UpdateProduct(UpdateView):
    model = Product
    form_class = UpdateProductForm
    def get_product_type_id(self):
        product = Product.objects.get(pk=self.kwargs['pk'])
        product_type_id = product.product_type.id
        return product_type_id
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy('products',
                            kwargs={'id': self.get_product_type_id()},
                            current_app='products')
    