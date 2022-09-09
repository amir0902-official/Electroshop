from django.urls import path

from .views import ProductDetailView, category_page, search

app_name = 'product'
urlpatterns = [
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:slug>', category_page, name='category'),
    path('search', search, name='search'),
]
