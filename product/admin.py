from django.contrib import admin

from .actions import export_products, make_active, make_inactive, export_as_json
from .models import Product, Category, Photo, Data


class PhotoAdmin(admin.StackedInline):
    model = Photo


class DataAdmin(admin.StackedInline):
    model = Data


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin, DataAdmin]
    actions = [export_products, export_as_json, make_active, make_inactive]
    list_display = ('name', 'categories_list', 'jpublish', 'humanize_price', 'quantity', 'status',)
    list_filter = ('publish', 'status')
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'slug', 'description', 'category', 'price', 'quantity', 'publish', 'related_products',)
        }),
        ('اطلاعات متا', {
            'fields': ('meta_title', 'meta_description',)
        }),
    )

    class Meta:
        model = Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'position', 'parent')
    list_filter = ('status',)
    actions = [make_active, make_inactive, export_as_json]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

