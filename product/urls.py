from django.urls import path

from .views import home, ProductDetailView

app_name = 'product'
urlpatterns = [
    path('', home, name='home'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product-detail'),
]
