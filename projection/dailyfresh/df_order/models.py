# coding=utf-8
from django.db import models


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20,primary_key=True)
    odate =models.DateTimeField(auto_now=True)
    # 用来判断是否支付
    oIspay = models.BooleanField(default=False)
    ouser = models.ForeignKey('df_user.UserInfo')
    oaddress = models.CharField(max_length=150)
    # 用来计算总的金额
    ototal = models.DecimalField(max_digits=6,decimal_places=2)

class OderDetailInfo(models.Model):
    good = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    count = models.IntegerField()