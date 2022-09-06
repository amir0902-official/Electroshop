from django.shortcuts import render

from blog.models import Article
from .models import Product


def home(request):
    newest_products = Product.objects.active()[:8]
    best_selling_products = None    #TODO Complete This After Cart Model
    context = {
        'newest_products': newest_products,
        'best_selling_products': best_selling_products,
        'latest_articles': Article.objects.filter(status='p')[:3],
    }
    return render(request, 'product/home.html', context)
