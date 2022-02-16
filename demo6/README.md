Django权限管理的实现
使用Django基于RBAC模式搭建权限管理功能。
## （一）django 权限机制
略
## （二）权限管理雏形
这里简单地将权限理解为对 URL 的访问能力。权限管理的生命周期如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/a2a8f847409546c2b05057669f70539c.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)


1，新建Django项目demo6，同时新建 名为app01的应用并注册。

2，在app01/models.py中建立权限表和用户表类：
```python
from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    url = models.CharField(max_length=64)
    title = models.CharField(max_length=10)

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Userinfor(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    permission = models.ManyToManyField(Permission, null=True, blank=True)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
```

 - 创建自定义的用户模型和权限模型，前者通过多对多关系关联到后者。

3，执行数据更新命令。

4，新建超级用户root，密码设置为root1234。


5，在app01/admin.py中注册这两个表，Permission和Userinfor：

```python
from Django.contrib import admin

from .models import Permission,Userinfor

# Register your models here.

admin.site.register(Permission)

admin.site.register(Userinfor)
```

6，运行demo6项目，访问 http://127.0.0.1:8000/admin ，如登录Django自带的admin后台。

7，增加权限记录：
![在这里插入图片描述](https://img-blog.csdnimg.cn/f3f515ac89fa48c38319c53b91678f96.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)

8，在用户表中新建两个用户记录user1和user2，其中给user1绑定查看用户1的权限，user2不绑定任何权限。
![在这里插入图片描述](https://img-blog.csdnimg.cn/392bfd5133e941eea90d99d8d9938bb2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/9b316e25d7634bdcb82039f8dc1b70c1.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
9，在app01/views.py内编写登录逻辑和访问、查看用户逻辑：

```python
from django.shortcuts import render, HttpResponse, redirect

from .models import Userinfor, Permission


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = Userinfor.objects.filter(name=username, pwd=pwd).first()
        if user:
            # 验证身份
            request.session["user_id"] = user.pk
            return HttpResponse('登录成功')
    return render(request, "login.html")


def userinfo(request):
    # 首先进行身份验证
    pk = request.session.get('user_id')
    if not pk:
        return redirect("/login/")
    # 然后进行权限验证
    user = Userinfor.objects.filter(id=pk).first()
    p_list = []
    p_queryset = user.permission.all()
    # 获取用户的权限列表
    for p in p_queryset:
        p_list.append(p.url)
    # 去重
    p_list = list(set(p_list))
    # print(p_list)
    # 获取URL
    c = request.path_info
    if c in p_list:
        u_queryset = Userinfor.objects.all()
        return render(request, "userinfo.html", {"u_queryset": u_queryset})
    else:
        return HttpResponse('没有权限访问该页面')
```

 - 登录中没使用内置的`authtication()`身份验证，而是直接将查出来的用户标识写入会话。
 - 没使用内置的`has_perm()`权限判断，

10，在demo6/urls.py内配置路由代码，而是直接查询当前用户是否用访问 URL 的权限。

```python
from django.contrib import admin
from django.urls import path

from app01.views import login,userinfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('userinfo01/', userinfo),
]
```
11，在templates目录下新建html文件login.html：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h4>用户登录</h4>
<form action="/login/" method="post">
    {% csrf_token %}
    <label>
        用户名：
        <input type="text" name="username">
    </label>
    <label>
        密码：
        <input type="password" name="pwd">
    </label>
    <input type="submit">
</form>
</body>
</html>
```
12，在templates目录下新建Html文件userinfo.html：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h4>用户</h4>
<ul>
    {% for user in u_queryset %}
        <li>{{ user.name }}</li>
    {% endfor %}
</ul>
</body>
</html>
```
13，访问http://127.0.0.1:8000/login/ 并登录 user1，成功后访问/userinfo01/路由：
![在这里插入图片描述](https://img-blog.csdnimg.cn/c33ebb4b97364805820cfe16dc2fb47d.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/26a997dc3fd54281a7097bdd1ed12067.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)

14，访问http://127.0.0.1:8000/login/ 并登录 user1，成功后访问/userinfo01/路由：
![在这里插入图片描述](https://img-blog.csdnimg.cn/021beecd385c4c7791dd3a07ad2e594d.png)

 - 与上一步相互佐证。

## （三）什么是RBAC
高耦合，可读性好，够精简，能完成项目需求。

但不合格。因为用户体验差，体现不出权限管理系统降低重复动作的作用。

相比于权限管理模式，在RBAC（Role-Based Access Control，基于角色的访问控制）的生命周期中增加了“角色”这个概念：
![在这里插入图片描述](https://img-blog.csdnimg.cn/1685f37534c94bce92f1f07acf07ddf3.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
RBAC生命周期介绍如下：

 1. 用户登录验证。
 2. 根据用户身份验证信息，获取用户的角色。
 3. 通过用户所绑定的角色（有可能不止一个），获取这个角色绑定的所有权限，并去重。
 4. 查询用户所访问的URL是否在角色的权限内，如果在，则继续访问，如果不在，则拒绝访问。


## （四）使用RBAC
给demo6增加RBAC的功能，实现角色权限管理的业务需求。

1，在demo6中新建名为rbac的App，并注册。

2，在rbac/model.py中新建权限管理所需的表类：

```python
from django.db import models


class Permission(models.Model):
    """
    权限表
    """
    url = models.CharField(max_length=64)
    title = models.CharField(max_length=10)

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=10)
    permission = models.ManyToManyField(Permission, null=True, blank=True)

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class User(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    role = models.ManyToManyField(Role, null=True, blank=True)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
```

3，注册用户表、权限表、角色表：

```python
from django.contrib import admin

from .models import User, Role, Permission

admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(User)
```
4，执行数据更新命令。

5，运行demo6项目，访问 http://127.0.0.1:8000/admin ，如登录Django自带的admin后台。

6，增加权限记录：
![在这里插入图片描述](https://img-blog.csdnimg.cn/dcced3d014d944dbbe42a736b76c2484.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
7，角色表里增加一条角色记录，角色：人力资源总监，权限：查看用户2。

![在这里插入图片描述](https://img-blog.csdnimg.cn/4e656ded5b2043eeb3e8e2bbbccf14a5.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
8，在用户表中新建两个用户记录user1和user2，其中给user1角色设定为人力资源总监，user2不设定任何角色。
![在这里插入图片描述](https://img-blog.csdnimg.cn/550202033aeb4d24ac33486908a1b65b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/5e403b80ead541178470e7efa498e0b2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)

9，重写app01/views.py中的login函数，login函数在“查询角色所对应的权限”环节，有两种写法。

```python
from django.shortcuts import render, HttpResponse, redirect

from rbac.models import User, Permission, Role


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get('pwd')
        user = User.objects.filter(name=username, pwd=pwd).first()
        # 先验证身份
        if user:
            request.session["user_id"] = user.pk
            # 查询角色
            ret = user.role.all()
            print(ret)  # <QuerySet [<Role: 人力资源总监>]>
            # 再查询角色所对应的权限
            re = user.role.all().values('permission__url')
            print(re)  # <QuerySet [{'permission__url': '/users/'}]>
            # 最后将所有权限写入会话
            permission_list = []
            for item in re:
                permission_list.append(item["permission__url"])
            print(permission_list)  # ['/users/']
            request.session["permission_list"] = permission_list

            return HttpResponse('登录成功')
    return render(request, "login.html")

# def login(request):
#     if request.method == "POST":
#         username=request.POST.get('username')
#         pwd=request.POST.get('pwd')
#         user=User.objects.filter(name=username,pwd=pwd).first()
#         if user:
#             #验证身份
#             request.session["user_id"]=user.pk
#             #查询角色
#             ret=user.role.all()
#             #print(ret)#<QuerySet [<Role: 人力资源总监>]>
#             #查询角色所对应的权限
#             permission_list = []
#             for item1 in ret:
#                 #多对多连表查询
#                 rep =Permission.objects.filter(role__title=item1)
#                 for item2 in rep:
#                     #print(item2.url)#/users/
#                     permission_list.append(item2.url)
#             print(permission_list)
#             request.session["permission_list"] = permission_list
#         return HttpResponse('登录成功')
#     return render(request, "login.html")
```
10，权限验证：在app01/views.py中，编写查看用户函数，内含权限验证代码。

```python
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
```
11，配置路径： 

```python
from django.contrib import admin
from django.urls import path

# from app01.views import login, userinfo
from rbac.views import login, user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    # path('userinfo01/', userinfo),
    path('users/', user),
]
```
13，访问http://127.0.0.1:8000/login/ 并登录 user1，成功后访问/users/路由：
![在这里插入图片描述](https://img-blog.csdnimg.cn/349472197ff841938a19fcb2f05213d6.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
![在这里插入图片描述](https://img-blog.csdnimg.cn/8086788a5698479bbb597b34c09cd132.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)


14，访问http://127.0.0.1:8000/login/ 并登录 user2，成功后访问/users/路由：
![在这里插入图片描述](https://img-blog.csdnimg.cn/ed657d464599435cb7f17ecd22994dcc.png)

## （五）基于中间件的权限验证
权限验证几乎是每个用户的数据请求都需要经历的过程。对于重复的系统级别的操作，有三种方法简化：

 - 给每一个视图函数都加一遍权限验证代码；
 - 写一个装饰器的封装权限验证逻辑，然后给每一个视图函数添加装饰器；
 - 将权限验证设置为中间件，即插即用。


1，在rbac目录下新建包service，然后在service目录下新建__init__.py文件和rbac.py文件，在rbac.py中编写权限验证中间件代码：

```python
import re

from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ValidPermission(MiddlewareMixin):
    """
    权限验证中间件类
    """

    def process_request(self, request):
        ######################中间件内容start###############
        # 获取session键值，如果不存在，不报错，返回[]
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
        ##################中间件内容end###################
        return None
```

2，在settings.py内配置中间件：

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'rbac.service.rbac.ValidPermission',
]
```
3，设置访问路径白名单：

```python
import re

from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ValidPermission(MiddlewareMixin):
    """
    权限验证中间件类
    """
    def process_request(self,request):
        ######################中间件内容start###############
        path = request.path_info
        #print(path)
        #查看是否属于白名单
        #valid_url_list=['/login/','/register/','/admin/.*']
        #for valid_url in valid_url_list:
        #     ret=re.match(valid_url,path)
        #     if ret:
        #         return None
        # 获取session键值，如果不存在，不报错，返回None
        permission_list = request.session.get('permission_list', [])
        #print(permission_list)
        flag = False
        for permission in permission_list:
            permission = "^%s$" % permission
            ret = re.match(permission, path)
            if ret:
                flag = True
                break
        #print(flag)
        if not flag:
            return HttpResponse('无访问权限！')
        ##################中间件内容end###################

        return None
```

 - 当我们想要换一个用户名登录时，访问： http://127.0.0.1:8000/login/ ，会发现在登录之前被要求权限验证。从逻辑上来说，应该先进行身份验证，再进行权限验证，如果没有身份验证，权限验证将无从谈起。所以，所有与身份验证相关的权限（URL），都不应该受到权限验证中间件的影响。我们将中间件代码加以优化，将登录、注册、后台管理相关的URL都加入白名单中。


4，在login视图函数中，查询角色和查询角色所对应的权限，应该属于权限校验，而非身份校验，这显然是存在耦合性过高的情况，应该将权限校验进行解耦。rbac/service下新建permission.py模块文件，同时修 login函数：

```python
from rbac.models import User, Permission, Role


def initial_permission(user, request):
    # 查询角色
    ret = user.role.all()
    # print(ret)#<QuerySet [<Role: 人力资源总监>]>
    # 查询角色所对应的权限
    permission_list = []
    for item1 in ret:
        # 多对多连表查询
        rep = Permission.objects.filter(role__title=item1)
        for item2 in rep:
            # print(item2.url)#/users/
            permission_list.append(item2.url)
    # print(permission_list)
    request.session["permission_list"] = permission_list
```