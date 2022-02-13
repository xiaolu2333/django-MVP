from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    mobile = models.CharField('手机号码', max_length=11)

    # 设置返回值
    def __str__(self):
        return self.username
