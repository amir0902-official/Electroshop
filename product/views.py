from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.core.paginator import Paginator

from blog.models import Article
from .models import Product, Category


def home(request):
    newest_products = Product.objects.active()[:8]
    best_selling_products = None    #TODO Complete This After Cart Model
    context = {
        'newest_products': newest_products,
        'best_selling_products': best_selling_products,
        'latest_articles': Article.objects.filter(status='p')[:3],
    }
    return render(request, 'product/home.html', context)


def category_page(request, slug):
    page_number = request.GET.get('page') or 1

    category = get_object_or_404(Category.objects.active(), slug=slug)
    products = category.products.active()

    paginator = Paginator(products, 2)
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'objects': page_obj,
    }
    return render(request, 'product/category.html', context)


class ProductDetailView(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product.objects.active(), slug=slug)
