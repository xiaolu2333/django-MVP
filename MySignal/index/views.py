# coding=gbk
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from index.models import ProductInfo, OrderInfo
from index.signals import signal_orders


# Create your views here.
def order_info(request):
    return render(request, 'order.html')


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        ProductID = int(request.POST.get('ProductID', ''))
        ProductQuantity = int(request.POST.get('ProductQuantity', ''))
        Check = request.POST.get('Check', '')
        create = request.POST.get('create', '')
        if Check == "on" and create == "create":
            if ProductID >= 1 and ProductQuantity >= 1:
                order = OrderInfo(product_id=ProductID, product_quantity=ProductQuantity)
                order.save()
                return HttpResponse("订单创建成功")
            else:
                return HttpResponse("请填写完整的订单信息！")
        else:
            return HttpResponse("请确认订单！")
    if request.method == "GET":
        return render(request, 'order.html')


@csrf_exempt
def cancel_order(request):
    if request.method == "POST":
        ProductID = int(request.POST.get('ProductID', ''))
        ProductQuantity = ProductInfo.objects.get(id=int(request.POST.get('ProductQuantity', '')))
        Check = request.POST.get('Check', '')
        cancel = request.POST.get('cancel', '')
        if Check == "on":
            if ProductID >= 1 and ProductQuantity:
                order = OrderInfo.objects.get(product_id=ProductID)
                if cancel == "cancel" and order.state == 1:
                    order.state = 0
                    order.save()
                    return HttpResponse('订单取消成功')
                else:
                    return HttpResponse('订单不符合取消条件')
            else:
                return HttpResponse("请填写完整的订单信息！")
        else:
            return HttpResponse("请确认订单！")
    if request.method == "GET":
        display = 'd-none'
        return render(request, 'order.html', locals())
