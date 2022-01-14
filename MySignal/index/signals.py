# coding=gbk
from django.db.models.signals import post_save
from index.models import OrderInfo, ProductInfo


# ���������ź�post_save�Ļص�����signal_post_save
def signal_orders(sender, **kwargs):
    print("pre_save is coming")
    # ���sender������
    print(sender)
    # instance����ǰ�޸Ļ�������ģ�Ͷ���
    instance = kwargs.get('instance')

    # ������״̬����0��ʱ��˵�������Ѿ�ȡ������Ʒ������
    if instance.state == 0:
        p = ProductInfo.objects.get(id=instance.product_id)
        p.number += instance.product_quantity
        p.save()
    # ������״̬����1˵����������������Ʒ������
    elif instance.state == 1:
        p = ProductInfo.objects.get(id=instance.product_id)
        p.number -= instance.product_quantity
        p.save()


# �������ź�post_save��ص�����signal_post_save��
post_save.connect(signal_orders, sender=OrderInfo)
