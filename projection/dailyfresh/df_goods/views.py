# coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator


def index(request):
    #显示最新的和最热的4条信息
    typelist =TypeInfo.objects.all()
    # 返回当前对象的所有商品的信息
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:3]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:3]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:3]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:3]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:3]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:3]
    content ={
        'title':'首页',
        'type0':type0,'type01':type01,
        'type1': type1, 'type11': type11,
        'type2': type2, 'type21': type21,
        'type3': type3, 'type31': type31,
        'type4': type4, 'type41': type41,
        'type5': type5, 'type51': type51,

    }

    return render(request,'df_goods/index.html',content)


# tid主奥用来判断用户点击的是哪个商品类;pindex用来接收需要显示的页数;sort主要用来判断是以什么样的方式进行排序
def list(request,tid,pindex,sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # print(type(sort))
    if sort == '1':#默认
        goods_list = GoodsInfo.objects.filter(gtype_id =int(tid)).order_by('-id')
    elif sort == '2':  # 价格
        goods_list = GoodsInfo.objects.filter(gtype_id =int(tid)).order_by('-gprice')
    elif sort == '3': # 人气
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    print(news[0].gpic)
    paginator = Paginator(goods_list,10)
    page = paginator.page(int(pindex))
    # print(page)
    content = {
        'title':'商品列表',
        'typeinfo':typeinfo,
        'paginator':paginator,
        'page':page,
        'sort':sort,
        'news':news,
    }
    return render(request,'df_goods/list.html',content)

# 得到某个商品的详细的信息
def site(request,id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick =goods.gclick+1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    content = {
        'title':goods.gtype.Ttitle,
        'id':id,
        'news':news,
        'goods':goods
    }
    response = render(request,'df_goods/detail.html',content)
    # 当我们点击完一个商品时将其id写到cookie中去
    # 点击完成商品时当，此时需要读取现在cookie中的值
    goods_ids = request.COOKIES.get('goods_ids','')
    # 将其转化为字符串
    goods_id = '%d'%goods.id
    # 判断是否是存在cookie，如果不存在则直接将其写入，若存在则需要进行相应的判断
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',') # 将其以逗号作为区分拆分成列表
        # 先判断在已有的cookie中是否存在现有的这个值，如果存在则先将其删除，再将其加入进去，以此来保证得到的是最新的浏览记录
        if goods_ids1.count('goods_id')>=1:
            goods_ids1.remove('goods_id')
        goods_ids1.insert(0,goods_id) # 将其加入到cookie中去
        # 如果现有的列表中的个数大于六个，需要将最后一个进行删除
        if len(goods_ids1)>=6:
            del goods_ids1[5]
        goods_ids=','.join(goods_ids1)# 将得到的列表用','拼接成为字符串 ['1','2','3']可以拼接成‘1,2,3’
    else:
        goods_ids = goods_id
    # 将得到的字符串以cookie的方式进行储存，以便于在用户中心进行相关的浏览信息的读取
    response.set_cookie('goods_ids',goods_ids)
    return response
