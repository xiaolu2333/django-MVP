# coding=gbk
"""
@Project ��demo6 
@File    ��rbac.py
@Author  ��Dang FuLin
@Version ��1.0
@Date    ��2022/2/15 20:03 
"""
import re

from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin


class ValidPermission(MiddlewareMixin):
    """
    Ȩ����֤�м����
    """
    def process_request(self, request):
        ######################�м������start###############
        path = request.path_info
        # print(path)
        # �鿴�Ƿ����ڰ�����
        valid_url_list = ['/login/', '/register/', '/admin/.*']
        for valid_url in valid_url_list:
            ret = re.match(valid_url, path)
            if ret:
                return None
        # ��ȡsession��ֵ����������ڣ�����������None
        permission_list = request.session.get('permission_list', [])
        # print(permission_list)
        flag = False
        for permission in permission_list:
            permission = "^%s$" % permission
            ret = re.match(permission, path)
            if ret:
                flag = True
                break
        # print(flag)
        if not flag:
            return HttpResponse('�޷���Ȩ�ޣ�')
        ##################�м������end###################

        return None
