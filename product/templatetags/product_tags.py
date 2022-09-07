from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag('product/partials/header.html')
def header(request):
    return {
        'categories': Category.objects.active(),
        'request': request
    }


@register.inclusion_tag('product/partials/link.html')
def link(request, link, link_name, content, classes):
    return {
        'request': request,
        'link_name': link_name,
        'link': link,
        'content': content,
        'classes': classes,
    }
