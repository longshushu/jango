# coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from . import user_decorator
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from django.core.paginator import Paginator,Page



def register(request):
    return render(request,'df_user/register.html',{'title':'用户注册'})
def register_handle(request):
    #接收注册传来的数据
    post = request.POST
    uname = post.get('user_name')
    pwd = post.get('pwd')
    cpwd = post.get('cpwd')
    email = post.get('email')
    # 判断两次的密码是否相等
    if pwd != cpwd:
        return redirect('/df_user/register')
    #对密码进行加密
    s1 = sha1()
    pwd1 =s1.update(pwd)
    pwd2 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname =uname
    user.upwd = pwd2
    user.uemail = email
    user.save()
    #注册成功转向登录页面
    return redirect('/df_user/login/')


# 动态的检测用户名是否存在
def register_exit(request):
    uname = request.GET.get('uname','')
    print(uname)
    count = UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count':count})


def login(request):
    uname = request.COOKIES.get('uname','')
    content = {'title':'用户登录','error_name':'0','error_pwd':'0','uname':uname}
    return render(request,'df_user/login.html',content)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 当去取‘jizhu'的值的时候，如果能够取到值就赋值，取不到值就用默认值0
    jizhu = post.get('jizhu','0')
    # 如果使用get的方式查询的话，当没有找到对象的时候会抛出异常，而如果使用filter进行查询的话，即使没有找到查询的对象也只是返回一个空的列表
    user = UserInfo.objects.filter(uname = uname) # 返回的是一个列表
    # print(user)
    # 对列表进行判断，如果列表不是空列表说明数据库里面存在该用户名，那么就进行下一步的密码的判断，反之直接抛出用户名错误
    if len(user)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == user[0].upwd:

            url = request.COOKIES.get('url','/df_goods/index')
            # 使用HttpResponseRedirect的主要原因是因为后续需要写入COOKIES，如果使用其他的话会造成后面的COOKIES不能写入
            red = HttpResponseRedirect(url)
            # 判断是否勾选记住密码
            if jizhu !=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            # 将得到的用户名缓存起来，便于后面的使用
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            print(request.session['user_name'])
            # 必须将得到的对象return出来，否则无法得到相应的对象
            return red

        else:
            content = {'title': '用户登录', 'error_name': '0', 'error_pwd': '1', 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', content)
    else:
        content = {'title': '用户登录', 'error_name': '1', 'error_pwd': '0', 'uname': uname,'upwd':upwd}
        return render(request,'df_user/login.html',content)
@user_decorator.login
def user_info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_ids1 =goods_ids.split(',')
    goods_list = []
    for good_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(pk=(good_id)))
    content = {
    'title':'用户中心',
    'user_name':request.session['user_name'],
    'user_email':user_email,
    'goods_list':goods_list,
    }
    return render(request,'df_user/user_center_info.html',content)


@user_decorator.login
def user_order(request,index):
    user_id = request.session['user_id']#读取到当前的用户的信息
    orderlist = OrderInfo.objects.filter(ouser_id = int(user_id)).order_by('-odate')
    #print(orderlist)
    paginator = Paginator(orderlist,2)#每一页显示2条数据
    page =paginator.page(int(index))
    content = {
        'title':'用户中心',
        'paginator':paginator,
        'page':page,
        'page_name': 1,
    }
    return render(request,'df_user/user_center_order.html',content)


@user_decorator.login
# 用户地址管理
def user_site(request):
    # 将当前登录的用户拿过来
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ureciver = post.get('receiver')
        user.uaddress = post.get('address')
        user.upost = post.get('postid')
        user.uphone = post.get('phone')
        user.save()
    content = {
        'title':'用户中心',
        'user':user
    }
    return render(request,'df_user/user_center_site.html',content)

def logout(request):
    request.session.flush()
    return render(request,'df_user/login.html')
