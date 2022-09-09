from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag('product/partials/header.html')
def header(request):
    return {
        'categories': Category.objects.active(),
        'request': request
    }
