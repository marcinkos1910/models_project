from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from store.models import Product


class StoreView(TemplateView):
    template_name = 'store/store.html'


def product(request, pk):
    p = Product.objects.filter(pk=pk).first()
    category = p.categories.prefetch_related().all()
    print(20 * '*')
    return render(request, 'store/product.html', context={'product': p, 'categories': category})


def product_list(request):
    products = Product.objects.all()
    print(20 * '%')
    return render(request, 'store/store.html', context={'products': products})


