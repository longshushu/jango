# coding=utf-8
from django.shortcuts import render,HttpResponse
from decimal import Decimal
from django.http import JsonResponse
from .models import *
from df_user.models import UserInfo
from df_cart.models import CartInfo
from  datetime  import datetime#订单提交时间
from django.db import transaction
import types

def order(request):
    uid = request.session['user_id']
    #取得当前的用户信息
    user = UserInfo.objects.get(id = uid)
    # 获取得到传过来的购物车的id,使用getlist可以得到一个列表
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    # 用来计算所有的价格
    total_price = 0
    # 将得到的购物车的信息取出来
    for cart_id in cart_ids:
        cart = CartInfo.objects.get(id = cart_id)
        carts.append(cart)
        total_price = total_price+float(cart.count)*float(cart.good.gprice)
    total_price = float('%0.2f'%total_price)
    value = datetime.now()
    trans_cost = 10
    total = total_price+trans_cost
    content = {
        'title':'提交订单',
        'user':user,
        'carts':carts,
        'total_price':total_price,
        'trans_cost':trans_cost,
        'total':total,
        'value':value,
    }
    return render(request,'df_order/place_order.html',content)
@ transaction.atomic()
def order_handle(request):
    tran_id = transaction.savepoint()#设置事物的起点，当发生意外时可以回滚到此处
    user_id = request.session['user_id']
    cart_ids = request.POST.get('cartids')  # 用户提交的订单购物车，此时cart_ids为字符串，例如'1,2,3,'
    #print(type(cart_ids))
    cart_ids = str(cart_ids)
    #print(type(cart_ids))
    #print(cart_ids)
    cart_ids1 = cart_ids.split(',')
    #print(cart_ids)
    #print(cart_ids1)
    try:
        orderinfo = OrderInfo()
        now = datetime.now()
        #orderinfo.ouser = UserInfo.objects.get('user_id')
        orderinfo.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),user_id)# 得到订单的编号
        orderinfo.odate = now
        #print(orderinfo.oid)
        orderinfo.ototal = Decimal(request.POST.get('total'))  # 从前端获取的订单总价
        #print(request.GET.get('total'))
       # print(orderinfo.ototal)
        orderinfo.ouser_id = int(user_id)
        #print(11111)
        orderinfo.save()
        #print(11111)
        for cart_id in cart_ids1:
            #print(cart_ids1)
            # 得到的因为是一个字符串需要将其进行相应的转化转化成为一个列表
            cart = CartInfo.objects.get(pk = cart_id) # 根据购物车的id得到具体的购物车
            orderdetail = OderDetailInfo()
            orderdetail.order = orderinfo# 有外键将其两个进行关联
           # print(cart)
            goods = cart.good #取出相应的购物车中的具体的商品
            if cart.count <= goods.gkucun:#如果购物车中的商品的数量小于等于商品的库存，修改数据库的数量
                goods.gkucun = goods.gkucun - cart.count #将商品的库存减去购物车中的数量得到现在商品的数量
                goods.save()
                orderdetail.good = goods
                orderdetail.price = goods.gprice
                orderdetail.count = cart.count
                orderdetail.save()
                cart.delete()# 当提交订单成功后对其对应的购车进行删除
            else:# 否则的话进行事务的回滚，跳回到起点，订单取消
                transaction.savepoint_rollback(tran_id)
                return HttpResponse('库存不足')
        data = {
            'ok':1,
        }
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        transaction.savepoint_rollback(tran_id)# 当出现任何的异常时都进行事务的回滚

    return JsonResponse(data)