import random
import time
import hashlib
import datetime
from Seller.models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect, HttpResponse


# Create your views here.
def login_valid(func):
    def inner(request, *args, **kwargs):
        cookie_username = request.COOKIES.get("username")
        session_username = request.session.get("username")
        if cookie_username and session_username and cookie_username == session_username:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Seller/login/")

    return inner


# 使用md5加密密码
def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def register(request):
    error_message = ""
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        code = request.POST.get("valid_code")
        # 检测有没有email
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                new_user = User()
                new_user.email = email
                # 用户名为邮箱
                new_user.username = email
                new_user.password = set_password(password)
                # 获取验证码
                valid_code = ValidCode.objects.filter(code_email=email).order_by("-code_time").first()
                # 将时间转换为时间戳的形式
                now = time.mktime(datetime.datetime.now().timetuple())
                code_time = time.mktime(valid_code.code_time.timetuple())
                times = (now - code_time) / 60
                # 检验验证码是否存在，是否被使用，是否过期，是否正确
                if valid_code and valid_code.code_status == 0 and times <= 5 and code.upper() == valid_code.code_content.upper():
                    valid_code.code_status = 1
                    valid_code.save()
                    new_user.save()
                else:
                    error_message = "验证码输入不正确"
            else:
                error_message = "邮箱已经被注册，请登录！"
        else:
            error_message = "邮箱不能为空！"

    return render(request, 'seller/register.html', locals())


def login(request):
    error_message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                # db_password = user.password
                password = set_password(password)
                if password == user.password:
                    response = HttpResponseRedirect("/Seller/index/")
                    response.set_cookie("username", user.username)
                    response.set_cookie("user_id", user.id)
                    request.session["username"] = user.username
                    return response
                else:
                    error_message = "密码错误"
            else:
                error_message = "用户名不存在"
        else:
            error_message = "邮箱不能为空"
    return render(request, 'seller/login.html', locals())


@login_valid
def index(request):
    return render(request, "seller/index.html", locals())


def logout(request):
    response = HttpResponseRedirect('/Seller/index/')
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session["username"]
    return response



@login_valid
def goods_list(request, page, status):
    # 直接获取数据
    # goods_list = Goods.objects.all()
    # 添加分页功能
    if status == "1":
        goods = Goods.objects.filter(goods_status=1)
    elif status == "0":
        goods = Goods.objects.filter(goods_status=0)
    else:
        goods = Goods.objects.all()
    # 进行分页，每页显示10条数据
    all_goods = Paginator(goods, 10)
    goods_list = all_goods.page(int(page))
    return render(request, 'seller/goods_list.html', locals())


def goods_status(request, state, id):
    id = int(id)
    goods = Goods.objects.get(id=id)
    if state == "up":
        goods.goods_status = 1
    elif state == "down":
        goods.goods_status = 0
    goods.save()
    # META.HTTP_REFERENCE:指出请求来源，上架或下载操作之后返回到原来的页面，没有来源，就返回到第一页
    url = request.META.get("HTTP_REFERENCE", "/goods_list/1/1/")
    return HttpResponseRedirect(url)


def personal_info(request):
    user_id = request.COOKIES.get("user_id")
    user = User.objects.get(id=int(user_id))
    user.username = request.POST.get("username")
    user.gender = request.POST.get("gender")
    user.phone_number = request.POST.get("phone_number")
    user.photo = request.POST.get("photo")
    user.address = request.POST.get("address")
    user.username = request.POST.get("username")
    return render(request, "seller/personal_info.html", locals())


def goods_add(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        goods = Goods()
        # 常规保存
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_date = data.get("goods_safe_date")
        goods.goods_produce_time = data.get("goods_produce_time")
        goods.goods_status = 1
        # 保存图片
        goods.goods_picture = files.get("picture")
        # 保存外键类型
        goods_type_id = int(data.get("goods_type"))
        goods.goods_type = GoodsType.objects.get(id=goods_type_id)
        # 保存对应卖家
        user_id = request.COOKIES.get("user_id")
        goods.goods_store = User.objects.get(id=int(user_id))

        goods.save()

    return render(request, 'seller/goods_add.html', locals())


# 9月17号
import json
import requests
from Qshop.settings import DING_URL

# 使用钉钉发送验证码
# def ding_send_message(content, to="18737616537"):
#     headers = {
#         "Content-Type": "application/json",
#         "Charset": "utf-8"
#     }
#     request_data = {
#         "msgtype": "text",
#         "text": {"content": content},
#         "at": {"atMobiles": [""], "isAtAll": True}
#     }
#     if to:
#         request_data["at"]["atMobiles"].append(to)
#         request_data["at"]["isAtAll"] = False
#     else:
#         request_data["at"]["atMobiles"].clear()
#         request_data["at"]["isAtAll"] = True
#     send_data = json.dumps(request_data)
#     response = requests.post(url=DING_URL, headers=headers, data=send_data)
#     content = response.json()
#     return content


import smtplib
from email.mime.text import MIMEText


# 使用邮箱发送验证码
def email_send_message(content):
    subject = "验证您的优就业管理系统"
    content = content
    sender = "dzlzhenyang@163.com"
    recver = "1510077642@qq.com"
    password = "dzl123456"
    message = MIMEText(content, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recver
    # 发送邮件
    smtp = smtplib.SMTP_SSL("smtp.163.com", 994)
    smtp.login(sender, password)
    smtp.sendmail(sender, recver.split(".\n"), message.as_string())
    smtp.close()
    return content


# 使用手机短信发送验证码 没搞好。。
def mobile_send_message(content):
    url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"
    account = "C80004177"
    password = "88b90f11cb20b6e10fbf31005bafe4f1"
    mobile = 18737616537
    content = "您的验证码是：%s。请不要把验证码泄露给其他人。" % content
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    # 构建发送参数
    data = {
        "account": account,
        "password": password,
        "mobile": mobile,
        "content": content
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.content.decode())
    return content


# 生成6位的验证码
def random_code(len=6):
    string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # "".join()将列表变成字符串
    valid_code = "".join([random.choice(string) for i in range(len)])
    return valid_code


# 在tasks中导入ding_send_message
from CeleryTask.tasks import ding_send_message
from django.views.decorators.csrf import csrf_exempt


# 保存验证码
@csrf_exempt
def send_valid_code(request):
    result = {
        "code": 200,
        "data": ""
    }
    if request.method == "POST":
        email = request.POST.get("email")
        code = random_code()
        valid_code = ValidCode()
        valid_code.code_email = email
        valid_code.code_content = code
        valid_code.save()
        send_data = "%s，您的验证码为%s，请不要将验证码泄露给其他人" % (email, code)
        # 发送验证
        ding_send_message.delay(send_data)
        # ding_send_message(send_data)
        result["data"] = "发送成功"
    else:
        result["code"] = 400
        result["data"] = "请求错误"
    return JsonResponse(result)


from Buyer.models import *


def order_list(request, status):
    # 获取店铺id
    user_id = request.COOKIES.get("user_id")
    # 获取店铺信息
    store = User.objects.get(id=int(user_id))
    # 获取店铺对应的所有订单
    order_list = store.orderdetail_set.filter(order_status=int(status)).order_by("-id")
    return render(request, "seller/order_list.html", locals())
