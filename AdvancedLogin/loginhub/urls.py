# coding=gbk
"""
@Project ：MyLogin 
@File    ：urls.py
@Author  ：Dang FuLin
@Version ：1.0
@Date    ：2022/2/12 19:35 
"""
from django.urls import path
from loginhub.views import indexView, loginView, registerView, logoutView

urlpatterns = [
    path('', indexView, name='index'),
    path('register/', registerView, name='register'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
]
