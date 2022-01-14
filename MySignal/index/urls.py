from django.urls import path
from index.views import order_info, create_order, cancel_order

urlpatterns = [
    # 定义路由
    path('create/', create_order, name='create'),
    path('cancel/', cancel_order, name='cancel'),
]
