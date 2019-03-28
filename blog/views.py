from django.shortcuts import render, HttpResponse, redirect
from PIL import Image, ImageFont, ImageDraw
import random
import string
from io import BytesIO
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import JsonResponse
from blog.forms import *
from .models import *

# Create your views here.


def login(request):
    if request.is_ajax():
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        valid_str = request.session.get("valid_str")
        print("user:", user, " pwd:", pwd, " code:", valid_code, " session_code:",valid_str)
        res = {"state": False, "msg": None}
        if valid_code.upper() == valid_str[0].upper():
            user_obj = authenticate(username=user, password=pwd)
            if user_obj:
                res["state"] = True
                auth.login(request, user_obj)
            else:
                res["msg"] = "用户名或密码错误"
        else:
            res["msg"] = "验证码错误"
        return JsonResponse(res)
    return render(request, "login.html")


def get_valid_img(request):
    valid_str = []

    # 随机数字和字母a-z A-Z 0-9
    def rndChar():
        global ret
        ret = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        valid_str.append(ret)
        return ret

    # 随机颜色1:
    def rndColor():
        return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)

    # 随机颜色2:
    def rndColor2():
        return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)

    # 160 x 59:
    width = 160
    height = 59
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:
    font = ImageFont.truetype("/BBS/static/my_ttf.ttf", 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    draw.text((20, 10), rndChar(), font=font, fill=rndColor2())
    # 模糊:
    # image = image.filter(ImageFilter.BLUR)

    f = BytesIO()
    image.save(f, 'jpeg')
    data = f.getvalue()
    f.close()

    request.session["valid_str"] = valid_str

    return HttpResponse(data)


def index(requset):
    article_list = Article.objects.all()
    return render(requset, "index.html", {"article_list": article_list})


def reg(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        res = {"user": None, "error_dict": None}
        if form.is_valid():
            user = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            re_pwd = form.cleaned_data.get("repeat_pwd")
            tel = form.cleaned_data.get("telephone")
            email = form.cleaned_data.get("email")
            head_image = request.FILES.get("header_image")
            print(user, "-", pwd, "-", re_pwd, "-", tel, "-", email, "-", head_image)
            if head_image:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=tel, avatar=head_image)
            else:
                user = UserInfo.objects.create_user(username=user, password=pwd, email=email, telephone=tel)
            res["user"] = user.username
        else:
            res["error_dict"] = form.errors
        return JsonResponse(res)
    form = RegForm()
    return render(request, "reg.html", locals())


