# coding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect


def login(func):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return func(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/df_user/login/')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun

'''
128.0.0.1:8080/1234/?type=1
使用get.path：表示的是当前的路径，得到的路径为/1234/
使用get_full_path：表示完整的路径，得到的是/1234/？type=1
'''