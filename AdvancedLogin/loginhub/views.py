from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import hashers, authenticate, login, logout
from django.urls import reverse

from loginhub.forms import LoginForm, RegisterForm
from loginhub.models import MyUser
from loginhub.utils.cookie import set_cookies


def indexView(request):
    login_flag = False
    if request.user.is_authenticated:
        login_flag = True
    return render(request,
                  'index.html',
                  {'login_flag': login_flag})

# 使用表单实现用户登录
def loginView(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)  # 身份认证
            if user is not None:
                # 登录
                login(request, user)
                return redirect(reverse("loginhub:index"))
    login_form = LoginForm()
    return render(request,
                  'login.html',
                  {'login_form': login_form})

def logoutView(request):
    logout(request)
    return redirect(reverse("loginhub:index"))

# 使用表单实现用户注册
def registerView(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.cleaned_data.pop('confirm_password')  # 清楚该字段
            register_form.cleaned_data['password'] = hashers.make_password(
                register_form.cleaned_data['password'])  # 密码加密
            user = MyUser(**register_form.cleaned_data)  # 实例化模型
            try:
                user.save()  # 保存模型实例
            except IntegrityError:  # 捕获整合错误：因为User 模型默认 username 保持唯一性
                raise ValidationError(  # 抛出注册表单自定义的异常
                    register_form.error_messages['username_existed']
                )
            return redirect(reverse("loginhub:index"))
    register_form = RegisterForm()
    return render(request,
                  'register.html',
                  {'register_form': register_form})
