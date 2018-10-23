from django.db import models

class CartInfo(models.Model):
    good = models.ForeignKey('df_goods.GoodsInfo')
    user = models.ForeignKey('df_user.UserInfo')
    count = models.IntegerField()

