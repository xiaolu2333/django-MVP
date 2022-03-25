from django.shortcuts import redirect
from django.urls import reverse


# µÇÂ½×°ÊÎÆ÷
def login_require(redirect_url_name=None):
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
