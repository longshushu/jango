# coding=utf-8
from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    Ttitle = models.CharField(max_length=20)
    IsDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.Ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    IsDelete = models.BooleanField(default=False)
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()
    gunit = models.CharField(max_length=20,default='500g')
    # 用富文本来呈现内容，便于用户进行相关的操作
    gdetail =HTMLField()
    gtype = models.ForeignKey(TypeInfo)