from django.core.paginator import Paginator
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
    category = Category.objects.get(slug=slug)
    category_post = Post.objects.filter(category=category)

    page = request.GET.get('page', '1')  # 페이지
    paginator = Paginator(category_post, 3)
    page_obj = paginator.get_page(page)

    return render(
        request,
        'blog/category_detail.html',
        {
            'category': category,
            'category_post': page_obj,
         }
    )
