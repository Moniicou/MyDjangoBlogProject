from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
import markdown
from django.views.generic.detail import SingleObjectMixin
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from comments.forms import CommentModelForm
from .models import Post, Category, Tag
from .utils import custom_paginator
# Create your views here.


def index(request):
    post_list = Post.objects.all()
    # 对post_List进行分页
    paginator = Paginator(post_list, 3)
    # 从request中获取page
    page = request.GET.get('page', None)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 给第一页
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # 把页对象返回
    return render(request, 'blog/index.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 从context中获取我们需要的数据
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        # 获取当前页page_obj.number
        start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=4)
        context.update({
            'page_range': range(start, end+1)
        })
        return context




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown.markdown(post.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify)
    ])
    form = CommentModelForm()
    # 评论列表
    comment_list = post.comment_set.all()

    # 调用阅读数增加的方法
    post.increase_views()

    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'comment_list': comment_list})


# 将detail函数转换成通用类视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    # 重写get方法，以调用increase_view方法
    def get(self, request, *args, **kwargs):
        # 先调用父类的get方法
        response = super().get(request, *args, **kwargs)
        # 调用increase_view方法
        self.object.increase_views()
        # 最后别忘了返回response
        return response

    # 重写get_object方法，为了使用markdown渲染post的content
    def get_object(self, queryset=None):
        # 调用父类的get_object，以获取对象
        self.object = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        self.object.content = md.convert(self.object.content)
        self.object.toc = md.toc
        # 返回object
        return self.object

    # 重写get_context_data方法，放入我们自己的上下文
    def get_context_data(self, **kwargs):
        # 调用父类的get_context_data方法，以获取当前context对象
        context = super().get_context_data(**kwargs)

        # 分页
        comment_list = self.object.comment_set.all()
        # 对post_List进行分页
        paginator = Paginator(comment_list, 3)
        # 从request中获取page
        page = self.request.GET.get('page', None)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            # 给第一页
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        start, end = custom_paginator(current_page=comments.number, num_pages=paginator.num_pages, max_page=4)
        context.update({
            'form': CommentModelForm(),
            'comments': comments,
            'page_range': range(start, end + 1),
        })
        # 返回context
        return context


# 优化PostDetailView
class PostDetailViewPrime(SingleObjectMixin, ListView):
    template_name = 'blog/detail.html'
    paginate_by = 1

    # 重写get方法
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 调用increase_views
        self.object.increase_views()
        return super().get(request, *args, **kwargs)

    # 重写get_object
    def get_object(self, queryset=Post.objects.all()):
        post = super().get_object(queryset=Post.objects.all())
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify)
        ])
        post.content = md.convert(post.content)
        post.toc = md.toc
        # 返回object
        return post

    # 重写get_context_data方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 从context中获取我们需要的数据
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        # 获取当前页page_obj.number
        start, end = custom_paginator(current_page=page_obj.number, num_pages=paginator.num_pages, max_page=4)
        context.update({
            'form': CommentModelForm(),
            'page_range': range(start, end + 1),
        })
        return context

    # 重写get_queryset
    def get_queryset(self):
        return self.object.comment_set.all()



# 归档
class ArchivesListView(PostListView):
    def get_queryset(self):
        return super().get_queryset().filter(created_time__year=self.kwargs['year'], created_time__month=self.kwargs['month'])


# 分类
class CategoriesListView(PostListView):
    def get_queryset(self):
        return super().get_queryset().filter(category_id=self.kwargs['pk']).order_by('-created_time')


# 标签云
class TagListView(PostListView):
    def get_queryset(self):
        # 先根据id取出tag对象
        # tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags__id=self.kwargs.get('pk')).order_by('-created_time')


def search(request):
    q = request.GET.get('q', None)
    # 判断能不能获取到搜索关键字
    if q:
        # 进行搜索
        # 根据q进行字段过滤
        object_list = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))
        # 返回首页
        return render(request, 'blog/index.html', {'object_list': object_list})
    else:
        msg = '请输入要搜索的内容！'
        return render(request, 'blog/index.html', {'msg': msg})
