from django.shortcuts import redirect
from django.urls import reverse


# cookieµÇÂ½×°ÊÎÆ÷
def cookie_login_required(redirect_url_name=None):
    def _decorator(func):
        def wrapper(request):
            username = request.COOKIES.get('username')
            if username:
                return func(request)
            else:
                if redirect_url_name:
                    return redirect(reverse(f"loginhub:{redirect_url_name}"))
                redirect(reverse("loginhub:login"))

        return wrapper

    return _decorator


# session µÇÂ½×°ÊÎÆ÷
def session_login_required(redirect_url_name=None):
    def _decorator(func):
        def wrapper(request):
            is_login = request.session.get('is_login','')
            if is_login:
                return func(request)
            else:
                if redirect_url_name:
                    return redirect(reverse(f"loginhub:{redirect_url_name}"))
                redirect(reverse("loginhub:login"))

        return wrapper

    return _decorator