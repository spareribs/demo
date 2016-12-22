from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from todolist.forms import TodolistaddForm
from todolist.models import Todolist
import datetime
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
import datetime


# Create your views here.
def todolist(request):
    todolist_lists = Todolist.objects.order_by("-id")

    limit = 3  # 每页显示的记录数
    paginator = Paginator(todolist_lists, limit)  # 实例化一个分页对象
    page = request.GET.get('page')
    try:
        todolist_lists = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        todolist_lists = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        todolist_lists = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'todolist.html', locals())


def add_todolist(request):
    if request.method == "POST":
        body = request.POST['body']
        add_date = datetime.datetime.now()
        tag_type = 0
        print(add_date)
        if body:
            Todolist.objects.create(
                body=body,
                add_date=add_date,
                tag_type=tag_type,
            )
        return HttpResponseRedirect('/todolist/')
    else:
        return HttpResponseRedirect('/todolist/')


def del_todolist(request):
    rowid = request.GET['rowid']
    Todolist.objects.filter(id=rowid).delete()
    return HttpResponse('{"code":0}')


def edit_todolist(request):
    rowid = request.POST['rowid']
    todolist_id = Todolist.objects.get(id=rowid)
    todolist_id.body = request.POST['body']
    todolist_id.save()
    return HttpResponseRedirect('/todolist/')


def chk_todolist(request):
    rowid = request.GET['rowid']
    todolist_id = Todolist.objects.get(id=rowid)
    todolist_id.tag_type = request.GET['status']
    todolist_id.save()
    return HttpResponse('{"code":0}')