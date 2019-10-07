from django.db import models
from Seller.models import User


# 订单表
class Order(models.Model):
    order_number = models.IntegerField()
    order_data = models.DateField(auto_now=True)
    order_money = models.FloatField(blank=True, null=True)
    # 订单对应的买家
    order_user = models.ForeignKey(to=User, on_delete=models.CASCADE)


# 订单详情表
class OrderDetail(models.Model):
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    order_status = models.IntegerField(default=0)
    goods_id = models.IntegerField()
    goods_name = models.CharField(max_length=32)
    goods_picture = models.CharField(max_length=32)
    goods_count = models.IntegerField()
    goods_price = models.FloatField()
    goods_total_price = models.FloatField()
    # 商品对应的卖家
    store_id = models.ForeignKey(to=User, on_delete=models.CASCADE)


# 购物车
class Cart(models.Model):
    goods_id = models.IntegerField()
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    # 购买数量
    goods_count = models.IntegerField()
    goods_picture = models.CharField(max_length=32)
    # 单个商品总价
    goods_total_price = models.FloatField()
    # 购物车对应的用户
    cart_user = models.IntegerField()
