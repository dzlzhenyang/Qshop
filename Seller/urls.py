from django.urls import path, re_path
from Seller.views import *

urlpatterns = [
    re_path(r'^$', index),
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('logout/', logout),
    re_path('goods_list/(?P<page>\d+)/(?P<status>[01])/', goods_list),
    re_path('goods_status/(?P<state>\w+)/(?P<id>\d+)/', goods_status),
    path('personal_info/', personal_info),
    # path('goods_add/', goods_add),
    path('send_valid_code/', send_valid_code),
    re_path(r'order_list/(?P<status>\d{1})', order_list),
]
