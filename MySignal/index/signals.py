# coding=gbk
from django.db.models.signals import post_save
from index.models import OrderInfo, ProductInfo


# 设置内置信号post_save的回调函数signal_post_save
def signal_orders(sender, **kwargs):
    print("pre_save is coming")
    # 输出sender的数据
    print(sender)
    # instance代表当前修改或新增的模型对象
    instance = kwargs.get('instance')

    # 当订单状态等于0的时候，说明订单已经取消，商品数量加
    if instance.state == 0:
        p = ProductInfo.objects.get(id=instance.product_id)
        p.number += instance.product_quantity
        p.save()
    # 当订单状态等于1说明订单是新增，商品数量减
    elif instance.state == 1:
        p = ProductInfo.objects.get(id=instance.product_id)
        p.number -= instance.product_quantity
        p.save()


# 将内置信号post_save与回调函数signal_post_save绑定
post_save.connect(signal_orders, sender=OrderInfo)
