from django import forms
import re
from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from blog.models import UserInfo

# 自定义手机号验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class RegForm(forms.Form):
    username = forms.CharField(max_length=10,
                               label="用户名",
                               widget=widgets.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(min_length=6,
                               label="密码",
                               widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True))
    repeat_pwd = forms.CharField(min_length=6,
                                 label="确认密码",
                                 widget=widgets.PasswordInput(attrs={"class": "form-control"}, render_value=True))
    telephone = fields.CharField(validators=[mobile_validate, ],
                                 label="手机号",
                                 error_messages={"required": "手机号不能为空"},
                                 widget=widgets.TextInput(attrs={"class": "form-control"}))
    email = fields.CharField(label="邮箱",
                             widget=widgets.EmailInput(attrs={"class": "form-control"}))

    def clean_username(self):
        val = self.cleaned_data.get("username")
        ret = UserInfo.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise ValidationError("该用户已存在")

    def clean(self):
        if self.cleaned_data.get("repeat_pwd") == self.cleaned_data.get("password"):
            return self.cleaned_data
        else:
            raise ValidationError("两次输入密码不一致")