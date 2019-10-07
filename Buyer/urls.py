from django.views.decorators.cache import cache_page
from django.urls import path, re_path
from Buyer.views import *

urlpatterns = [
    path('login/', login),
    path('index/', index),
    # 在登录页面设置缓存，存在时间为15分钟
    path('register/', register),
    path('goods_list/', goods_list),
    re_path('goods_details/(?P<id>\d+)/', goods_details),
    path('user_info/', user_info),
    path('logout/', logout),
    path('pay_order/', pay_order),
    path('alipay_order/', alipay_order),
    path('alipay_result/', alipay_result),
    path('add_cart/', add_cart),
    path('cart/', cart),
    path('get_task/', get_task),
    path('middle_ware_view/', middle_ware_view),
    path('middle_test_view/', middle_test_view),
    path('cache_test/', cache_test),
]
