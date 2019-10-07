from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32, null=True, blank=True)
    gender = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    photo = models.ImageField(upload_to="images", null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    # 0为买家，1为卖家，2为管理员
    user_type = models.IntegerField(default=0)


class GoodsType(models.Model):
    goods_type = models.CharField(max_length=32)
    goods_description = models.TextField()
    goods_type_picture = models.ImageField(upload_to="images", default="")


class Goods(models.Model):
    goods_number = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    goods_count = models.IntegerField()
    goods_location = models.CharField(max_length=254)
    goods_safe_date = models.IntegerField()
    goods_produce_time = models.DateField()
    # 0为下架，1为在售
    goods_status = models.IntegerField()

    goods_picture = models.ImageField(upload_to="images")
    goods_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE, default=1)
    goods_store = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)

    goods_details = models.ImageField(default="物美价廉，欢迎品尝")


class ValidCode(models.Model):
    code_content = models.CharField(max_length=32)
    code_email = models.EmailField()
    # 0位未使用，1为已使用
    code_status = models.IntegerField(default=0)
    code_time = models.DateTimeField(auto_now=True)
