from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article

# Create your views here.
class ArticleListView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'article_list'
    queryset = (Article.objects
                .select_related('author', 'category')
                .prefetch_related('tags')
                .defer('content')
                )