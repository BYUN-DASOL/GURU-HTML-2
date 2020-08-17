import math

from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator


class PostList(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()

        return context

class PostDetail(DetailView):
    model = Post


def PostListByCategory(request, slug):
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
    return render(request, 'blog/index.html', {
        'contacts' : contacts,
        'p_range' : p_range,
    })

# def document_list(request):
#     # documents = Document.objects.all()
#
#     page = int(request.GET.get('page', 1))
#
#     paginated_by = 2
#
#     documents = get_list_or_404(Document)
#
#     total_count = len(documents)
#     total_page = math.ceil(total_count/paginated_by)

# def post_detail(request, pk):
#     blog_post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'blog_post': blog_post,
#          }
#     )

# def index(request):
#     posts = Post.objects.all()
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )