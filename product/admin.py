from django.contrib import admin

from .actions import export_products
from .models import Product, Category, Photo, Data


class PhotoAdmin(admin.StackedInline):
    model = Photo


class DataAdmin(admin.StackedInline):
    model = Data


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin, DataAdmin]
    actions = [export_products]
    list_display = ('name', 'categories_list', 'publish', 'price', 'quantity', 'status',)

    class Meta:
        model = Product


admin.site.register(Photo)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

