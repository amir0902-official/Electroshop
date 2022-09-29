from django import template

from ..models import Category

register = template.Library()


@register.inclusion_tag('blog/partials/header.html')
def blog_header(request):
    return {
        'categories': Category.objects.all(),
        'request': request
    }
