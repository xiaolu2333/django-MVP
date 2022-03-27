1，创建项目，创建应用并注册。

2，安装依赖 djangorestframework、markdown、Django-filter 和 djangorestframework-simplejwt ，并注册与配置：

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 必须有
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JSONWebTokenAuthentication',
    ],
}

import datetime
JWT_AUTH = {
    # 指明Token的有效期
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}
```
3，提供用户可以获取和刷新 token 的 urls 地址，这两个 urls 分别对应 `TokenObtainPairView` 和 `TokenRefreshView` 两个视图。

```python
...
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT的认证接口
    path('jwt-token-auth/', obtain_jwt_token),
]
```
4，执行数据迁移，创建超级用户。

5，以 POST 方式向[http://127.0.0.1:8000/jwt-token-auth/](http://127.0.0.1:8000/jwt-token-auth/)提交用户名与密码，获得JWT：
![在这里插入图片描述](https://img-blog.csdnimg.cn/882efff549d34927a16dc909b3ba8896.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)


6，能获得 JWT 说明我们就能在接下来的任何需要身份认证的地方使用它，比如一个首页：
```python
from django.shortcuts import render, redirect, HttpResponse

from rest_framework.views import APIView


class IndexView(APIView):
	# 使用前面配置好的 JSONWebTokenAuthentication 作为默认后端
    def get(self, request):
        print(request)
        return HttpResponse('首页')
```
配置试图路由：

```python
...
	path('index/',IndexView.as_view(),name='index')
...
```
**对于不需要配置认证后端的逻辑，比如注册、登录、注销等，不应该使用JWT相关放入认证后端！**

7，以包含 JWT 的 Authorization 请求头的 GET 方式访问[http://127.0.0.1:8000](http://127.0.0.1:8000/j/)：

```python
{
	'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InVzZXIxIiwiZXhwIjoxNjQ4MzcwNDM4LCJlbWFpbCI6InVzZXIxQHVzZXIuY29tIn0.RVrB8mukA4p4iruZh_wTMTVaZFzjYG50rRPmVRI3uqA'
}
```
将获得需要 JWT 认证的视图的访问能力：
![在这里插入图片描述](https://img-blog.csdnimg.cn/541129da513441ddb841bd95a85644bd.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)
如果 JWT 错误，将无法访问：
![在这里插入图片描述](https://img-blog.csdnimg.cn/97652f52843045fcb82def6efe7f6d8f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAZGFuZ2Z1bGlu,size_20,color_FFFFFF,t_70,g_se,x_16)