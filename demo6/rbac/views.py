import re

from django.shortcuts import render, HttpResponse, redirect

from rbac.models import User, Permission, Role
from rbac.service.permission import initial_permission


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = User.objects.filter(name=username, pwd=pwd).first()
        if user:
            # 验证身份
            request.session["user_id"] = user.pk
            initial_permission(user, request)
            return HttpResponse('登录成功')
    return render(request, "login.html")


def user(request):
    # 获取session键值，如果不存在不报错，返回None
    permission_list = request.session.get('permission_list', [])
    # print(permission_list)
    path = request.path_info
    # print(path)
    flag = False
    for permission in permission_list:
        permission = "^%s$" % permission
        ret = re.match(permission, path)
        if ret:
            flag = True
            break
    # print(flag)
    if not flag:
        return HttpResponse('无访问权限！')
    return HttpResponse('查看用户')
