# coding=gbk
"""
@Project ��demo6 
@File    ��permission.py
@Author  ��Dang FuLin
@Version ��1.0
@Date    ��2022/2/16 13:03 
"""
from rbac.models import User, Permission, Role


def initial_permission(user, request):
    # ��ѯ��ɫ
    ret = user.role.all()
    # print(ret)#<QuerySet [<Role: ������Դ�ܼ�>]>
    # ��ѯ��ɫ����Ӧ��Ȩ��
    permission_list = []
    for item1 in ret:
        # ��Զ������ѯ
        rep = Permission.objects.filter(role__title=item1)
        for item2 in rep:
            # print(item2.url)#/users/
            permission_list.append(item2.url)
    # print(permission_list)
    request.session["permission_list"] = permission_list
