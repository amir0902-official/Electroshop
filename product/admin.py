from django.contrib import admin
from .models import Product, Category, Photo, Data


class PhotoAdmin(admin.StackedInline):
    model = Photo


class DataAdmin(admin.StackedInline):
    model = Data


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin, DataAdmin]

    class Meta:
        model = Product


admin.site.register(Photo)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

