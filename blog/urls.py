from django.urls import path

from .views import ArticleDetail


app_name = 'blog'
urlpatterns = [
    path('detail/<slug:slug>', ArticleDetail.as_view(), name='detail'),
]