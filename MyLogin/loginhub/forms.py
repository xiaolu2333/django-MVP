# coding=gbk
"""
@Project ：MyLogin 
@File    ：forms.py
@Author  ：Dang FuLin
@Version ：1.0
@Date    ：2022/2/12 19:32 
"""
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _


class RegisterForm(forms.Form):
    error_messages = {
        'username_existed': _('The same username already exists, please change it!'),
        'password_short': _('The length of password is less than 6!'),
        'password_mismatch': _('The two passwords are not the same!')
    }

    username = forms.CharField()
    email = forms.CharField(
        widget=forms.EmailInput()
    )
    mobile = forms.CharField()
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="密码至善需要六位！",
        strip=False,
    )
    confirm_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="密码至善需要六位！",
    )

    # min_length=6 会在前端对长度进行校验
    # def clean_password(self):
    #     if len(self.cleaned_data['password']) < 6:
    #         raise ValidationError(
    #             self.error_messages['password_short'],
    #         )
    #     return self.cleaned_data['password']

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise ValidationError(
                self.error_messages['password_mismatch'],
            )
        return self.cleaned_data['confirm_password']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="密码至善需要六位！",
        strip=False,
    )

    # 将身份验证放到视图中处理，这里就不再清洗数据
    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")
    #     authenticate
    # return self.cleaned_data

