# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from django.http import JsonResponse
from df_user import user_decorator


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    content = {
        'title':'购物车',
        'carts':carts,
    }
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    else:
        return render(request,'df_cart/cart.html',content)


@user_decorator.login
def add(request,gid,count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 将传过来的用户以及商品的信息在购物车中查询并返回
    carts = CartInfo.objects.filter(user_id = uid,good_id = gid)
    # 查询购物车中是否存在该商品，如果存在则只是进行数量上的增加，如果不存在则需要进行将商品加入到购物车中
    if len(carts)>=1:
        cart = carts[0]
        cart.count = cart.count+count
    else:
        cart = CartInfo()
        cart.good_id = gid
        cart.user_id = uid
        cart.count = count
    # 不管是修改 数据库的内容还是新建，都需要 对其进行相应的保存
    cart.save()
    # 此处的写法是用的是ajax，当用户点击购物车后不会跳转到购物车的页面，只会在购物车中进行内容的改变
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id = request.session['user_id']).count()
        return JsonResponse({'count': count})

    # 如果需要当点击完加入购物车后跳转到购物车的页面 就可以使用链接跳转的方式，此时的代码就直接是下面的代码
    else:
     return redirect('/df_cart/')


@user_decorator.login
def edit(request,cart_id,count):
    try:
        cart = CartInfo.objects.filter(id==cart_id)
        caount1 = cart.count=count
        cart.save()
        data={'ok':1}
    except Exception as e:
        data = {'ok':0}
    return JsonResponse(data)


@user_decorator.login
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.filter(id =int(cart_id))
        cart.delete()
        data = {'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)