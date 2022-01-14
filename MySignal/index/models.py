# coding=gbk
from django.db import models


class ProductInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    number = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '��Ʒ��Ϣ'
        verbose_name_plural = '��Ʒ��Ϣ'


STATE = (
    (0, 'ȡ��'),
    (1, '����'),
)


class OrderInfo(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()
    product_quantity = models.IntegerField()
    state = models.IntegerField(choices=STATE, default=1)

    def __str__(self):
        return id

    class Meta:
        verbose_name = '������Ϣ'
        verbose_name_plural = '������Ϣ'
