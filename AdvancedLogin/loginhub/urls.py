# coding=gbk
"""
@Project ：MyLogin 
@File    ：urls.py
@Author  ：Dang FuLin
@Version ：1.0
@Date    ：2022/2/12 19:35 
"""
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from loginhub.views import IndexView, loginView, registerView, logoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    # JWT的认证接口
    path('jwt-token-auth/', obtain_jwt_token),
]
