from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'djtools/blog/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'djtools/blog/post_detail.html'
