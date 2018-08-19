from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.views.generic import UpdateView

from users.forms import RegisterForm
from .models import User


def register(request):
    # 获取跳转地址
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    # 判断是什么提交方法
    form = RegisterForm()
    if request.method == 'POST':
        # 首先使用提交的数据生成form
        form = RegisterForm(request.POST, request.FILES)
        # 判断数据是否合法
        if form.is_valid():
            user = form.save()
            # 返回登录，并提示注册成功，请登录
            messages.success(request, '提示注册成功，请登录!')
            # 判断redirect_to是否存在。
            if redirect_to:
                login(request, user)
                return redirect(redirect_to)
            else:
                # 重定向到login
                return redirect(reverse('login'))
    else:
        return render(request, 'users/register.html', {'form': form, 'next': redirect_to})


class EditUserView(UpdateView):
    model = User
    fields = ['nickname', 'email', 'headshot', 'signature']
    success_url = reverse_lazy('blog:index')
