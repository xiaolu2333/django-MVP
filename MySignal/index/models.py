# coding=gbk
from django.db import models


class ProductInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    number = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'


STATE = (
    (0, '取消'),
    (1, '创建'),
)


class OrderInfo(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    product_quantity = models.IntegerField()
    state = models.IntegerField(choices=STATE, default=1)

    def __str__(self):
        return id

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = '订单信息'
