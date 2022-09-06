from django.contrib import admin
from django.contrib import messages

from product.actions import *
from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'jpublish', 'status', 'category_to_str',)
    list_filter = ('status', 'publish',)
    search_fields = ('title', 'description', 'category')
    ordering = ('status', '-publish')
    actions = ('make_published', 'make_draft', export_as_json)

    @admin.action(description='انتشار مقالات انتخاب شده')
    def make_published(self, request, queryset):
        updated = queryset.update(status='p')
        if updated == 1:
            msg = 'منتشر شد.'
        else:
            msg = 'منتشر شدند.'

        self.message_user(request, f'{updated} مورد {msg}', messages.SUCCESS)

    @admin.action(description='پیش نویس مقالات انتخاب شده')
    def make_draft(self, request, queryset):
        updated = queryset.update(status='d')
        if updated == 1:
            msg = 'پیش نویس شد.'
        else:
            msg = 'پیش نویس شدند.'

        self.message_user(request, f'{updated} مورد {msg}', messages.WARNING)


admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'slug', 'parent')
    actions = (make_active, make_inactive)


admin.site.register(Category, CategoryAdmin)
