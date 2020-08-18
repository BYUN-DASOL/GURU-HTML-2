import math

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .models import Post, Category
from django.views.generic import ListView, DetailView
from django.db.models import Q

class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()

        return context

class PostSearch(PostList):
    def get_queryset(self):
        q = self.kwargs['q']
        object_list = Post.objects.filter(Q(title__contains=q) | Q(content__contains=q))
        return object_list


class PostDetail(DetailView):
    model = Post



def PostListByCategory(request, slug):
    paginate_by = 4
    category = Category.objects.get(slug=slug)
    category_post = Post.objects.filter(category=category)

    return render(
        request,
        'blog/category_detail.html',
        {
            'category': category,
            'category_post': category_post,
         }
    )

def index(request):
    posts = Post.objects.all().order_by('-published_date')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    page_range = 5
    current_block = math.ceil(int(page)/page_range)
    start_block = (current_block-1) * page_range
    end_block = start_block + page_range
    p_range = paginator.page_range[start_block:end_block]
    return render(request, 'blog/category_detail.html', {
        'contacts': contacts,
        'p_range': p_range,
    })