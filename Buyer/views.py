import hashlib
from Seller.models import *
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse


def login_valid(func):
    def inner(request, *args, **kwargs):
        cookie_username = request.COOKIES.get("username")
        session_username = request.session.get("username")
        if cookie_username and session_username and cookie_username == session_username:
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")

    return inner


# 使用md5加密密码
def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


from django.views.decorators.cache import cache_page


# 设置缓存时间为60*15=900秒
#@cache_page(60 * 15)
# 买家登录功能
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username).first()
        # 判断user是否存在
        if user:
            db_password = user.password
            password = set_password(password)
            if db_password == password:
                response = HttpResponseRedirect('/Buyer/index')
                # 设置cookie和session
                response.set_cookie("username", user.username)
                response.set_cookie("user_id", user.id)
                request.session["username"] = user.username
                return response
    return render(request, 'buyer/login.html', locals())


# 买家注册功能
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User()
        user.username = username
        user.password = set_password(password)
        user.email = email
        user.save()
        return HttpResponseRedirect('/Buyer/login')
    return render(request, 'buyer/register.html', locals())


def index(request):
    # 查看所有类型
    all_goods_type = GoodsType.objects.all()
    result = []
    for goods_type in all_goods_type:
        # 外键查询
        goods = goods_type.goods_set.order_by("-goods_produce_time")
        if len(goods) >= 4:
            goods = goods[:4]
            result.append({"type": goods_type, "goods_list": goods})
    return render(request, 'buyer/index.html', locals())


def goods_list(request):
    # 获取请求的类型
    request_type = request.GET.get("type")
    # 获取关键字
    keywords = request.GET.get("keywords")
    # 定义返回的结果
    goods_list = []
    # t为类型查询
    if request_type == "t":
        if keywords:
            id = int(keywords)
            # 先查询类型
            goods_type = GoodsType.objects.get(id=id)
            # 再查询类型中的数据
            goods_list = goods_type.goods_set.order_by("-goods_produce_time")
    # k为关键字类型
    elif request_type == 'k':
        if keywords:
            # 使用name的模糊查询
            goods_list = Goods.objects.filter(goods_name__contains=keywords).order_by("-goods_produce_time")
    # 限定推荐的条数
    if goods_list:
        # 每行显示5个
        lenth = len(goods_list) / 5
        if lenth != int(lenth):
            lenth += 1
        lenth = int(lenth)
        recommend_list = goods_list[:lenth]
    return render(request, 'buyer/goods_list.html', locals())


def goods_details(request, id):
    goods = Goods.objects.get(id=int(id))
    return render(request, 'buyer/goods_details.html', locals())


@login_valid
def user_info(request):
    return render(request, 'buyer/user_info.html', locals())


def logout(request):
    url = request.META.get("HTTP_REFERER", '/Buyer/index')
    response = HttpResponseRedirect(url)
    for k in request.COOKIES:
        response.delete_cookie(k)
    del request.session["username"]
    return response


import time
from Buyer.models import *


# 9月11
# @login_valid
def pay_order(request):
    goods_id = request.GET.get("goods_id")
    goods_count = request.GET.get("goods_count")
    if goods_id and goods_count:
        # 保存订单表
        order = Order()
        order.order_number = str(time.time()).replace(".", "")
        user_id = request.COOKIES.get("user_id")
        order.order_user = User.objects.get(id=int(user_id))
        order.save()
        # 保存订单详情表
        # 先查询商品信息
        goods = Goods.objects.get(id=int(goods_id))
        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods.id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_picture = goods.goods_picture
        order_detail.goods_count = goods_count
        order_detail.goods_price = goods.goods_price
        order_detail.goods_total_price = goods.goods_price * int(goods_count)
        order_detail.store_id = goods.goods_store
        order_detail.save()
        order.order_money = order_detail.goods_total_price
        order.save()

    return render(request, 'buyer/pay_order.html', locals())


from alipay import AliPay
from Qshop.settings import alipay_private_key_string, alipay_public_key_string


def alipay_order(request):
    order_number = request.GET.get("order_number")
    order_total = request.GET.get("order_total")
    # 实例化支付
    alipy = AliPay(
        appid="2016101200667716",
        app_notify_url=None,
        app_private_key_string=alipay_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )
    # 实例化订单,网页支付的订单
    order_string = alipy.api_alipay_trade_page_pay(
        out_trade_no=order_number,  # 订单号
        total_amount=order_total,  # 支付金额
        subject="生鲜交易",  # 支付主题
        return_url="http://127.0.0.1:8000/Buyer/alipay_result/",
        notify_url="http://127.0.0.1:8000/Buyer/alipay_result/"
    )
    # 拼接收款地址 = 支付宝网关+ 订单返回参数
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)


def alipay_result(request):
    out_trade_no = request.GET.get("out_trade_no")
    if out_trade_no:
        order = Order.objects.get(order_number=out_trade_no)
        order.orderdetail_set.update(order_status=1)

    return render(request, "buyer/alipay_result.html", locals())


# 9月16
# 添加到购物车
@login_valid
def add_cart(request):
    result = {
        "code": 200,
        "data": ""
    }
    if request.method == "POST":
        goods_id = int(request.POST.get("goods_id"))
        goods_count = int(request.POST.get("goods_count", 1))
        # 获取商品信息
        goods = Goods.objects.get(id=goods_id)
        cart = Cart()
        cart.goods_id = goods_id
        cart.goods_name = goods.goods_name
        cart.goods_count = goods_count
        cart.goods_price = goods.goods_price
        cart.goods_picture = goods.goods_picture
        cart.goods_total_price = goods.goods_price * goods_count
        cart.cart_user = request.COOKIES.get("user_id")
        cart.save()
        result["data"] = "添加购物车成功！"

    else:
        result["code"] = 500
        result["data"] = "请求发生未知错误"

    return JsonResponse(result)


def cart(request):
    user_id = request.COOKIES.get("user_id")
    goods = Cart.objects.filter(cart_user=int(user_id)).order_by("-id")
    # 调用goods_count方法
    goods_count = goods.count()
    return render(request, 'buyer/cart.html', locals())


# 9月18号
from CeleryTask.tasks import add


def get_task(request):
    num1 = request.GET.get("num1", 1)
    num2 = request.GET.get("num2", 2)
    # 发布任务
    add.delay(int(num1), int(num2))
    # 返回一个JsonResponse对象
    return JsonResponse({"data": "success"})


def middle_ware_view(request):
    print("我是view")
    return JsonResponse({"data": "success"})


from django.http import HttpResponse


def middle_test_view(request):
    def hello():
        return HttpResponse("hello world")

    rep = HttpResponse("ni hao")
    rep.render = hello
    return rep


from django.core.cache import cache


def cache_test(request):
    # 从缓存中获取数据
    user = cache.get("user")
    if not user:
        user = User.objects.get(id=5)
        # 将用户数据存入缓存，缓存时间为30秒
        cache.set("user", user, 30)
    return JsonResponse({"data": "success"})
