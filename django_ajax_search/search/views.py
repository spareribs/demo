# -*- coding:utf-8 -*-
from django.shortcuts import render
from search.models import Cnword
from django.http import HttpResponse
import json


# 访问主页
def index(request):
    return render(request, 'index.html')


# 输入内容简单搜索
def search(request):
    # 获取Ajax POST过来的kw的数据
    kw = request.GET.get('kw')
    # 从数据库中查询出10条记录【QuerySet对象】
    word = Cnword.objects.filter(words__startswith=kw).values('words')[0:10]
    word = list(word)  # ValuesQuerySet对象需要先转换成list
    data = json.dumps(word)  # 把list转成json
    return HttpResponse(data)  # 返回json


# 显示词条的具体搜索
def match(request):
    str_kw = request.GET.get('kw')
    unicode_kw = str_kw.encode()
    print(unicode_kw)
    word = Cnword.objects.filter(words=unicode_kw).values('explain')
    print(word)
    word = list(word)
    data = json.dumps(word)
    return HttpResponse(data)
