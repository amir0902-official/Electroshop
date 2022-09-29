from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from .models import Article, Category


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)
