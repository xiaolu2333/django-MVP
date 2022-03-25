# coding=gbk
"""
@Project ：AdvancedLogin 
@File    ：cookie.py
@Author  ：Dang FuLin
@Version ：1.0
@Date    ：2022/3/25 18:08 
"""
import datetime

from django.conf import settings


def set_cookies(response, key=None, value='', mapping=None, expire=None):
    """
    设置 cookies 及其存活时间
    :param response: Response对象
    :param key: cookie key
    :param value: cookie value
    :param mapping: cookie key-value
    :param expire: expire, seconds
    """
    if expire is None:
        max_age = 24 * 60 * 60  # 默认max_age为一天
    else:
        max_age = expire
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")

    if key is None and not mapping:
        raise Exception("必须添加cookie参数")
    items = []
    if key is not None:
        items.extend((key, value))
        response.set_signed_cookie(key, value, max_age=max_age, expires=expires,
                                   domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
    if mapping is not None:
        for pair in mapping.items():
            response.set_signed_cookie(pair[0], pair[1], max_age=max_age, expires=expires,
                                       domain=settings.SESSION_COOKIE_DOMAIN,
                                       secure=settings.SESSION_COOKIE_SECURE or None)


def delete_cookies(response, key=None, mapping=None):
    """
    删除 cookies
    :param response: Response对象
    :param key: cookie key
    :param mapping: cookie key-value
    """
    if key:
        response.delete_cookie(key)
    if mapping:
        for pair in mapping.items():
            response.delete_cookie(pair[0])


# if __name__ == '__main__':
#     pass
