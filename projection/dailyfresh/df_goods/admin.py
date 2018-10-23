from django.contrib import admin
from models import *


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','Ttitle']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id','gtitle','gprice','gunit','gclick','gkucun','gjianjie','gdetail','gtype']


admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodsInfo,GoodsInfoAdmin)