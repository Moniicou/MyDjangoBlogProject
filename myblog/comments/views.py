from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import CreateView

from blog.models import Post
from .forms import CommentModelForm
from .models import Comment
# Create your views here.


# 处理提交评论
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentModelForm()
    # 只处理post方法的提交
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        # 校验form表单
        if form.is_valid():
            comment = form.save(commit=False)
            # 把确实的信息，即comment所属的post
            comment.post_id = pk
            comment.save()
        else:
            context = {
                'post': post,
                'form': form,
                'comment_list': post.comment_set.all()
            }
            return render(request, 'blog/detail.html', context)
    return redirect(post)


# 改成通用类视图
class CommentCreateView(CreateView):
    model = Comment
    fields = ['name', 'email', 'url', 'content']
    template_name = 'blog/detail.html'
    context_object_name = 'comment_list'

    # 重写get_success_url方法
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs.get('pk')})

    # 重写form_valid方法，补全comment需要的post
    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        return super().form_valid(form)

    # 重写get_context_data方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 往context中添加我们自己的上下文
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        context.update({
            'post': post,
            'comment_list': post.comment_set.all()
        })
        # 返回
        return context

    # 当form表单校验不通过时，执行form_invalid方法
    def form_invalid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return render(self.request, 'blog/detail.html', {
            'post': post,
            'comment_list': post.comment_set.all()
        } )
