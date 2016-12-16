# 概述
## 实验要求
> 使用ajax实现百度搜索自动补全的功能，具体要求如下：
1. 使用jquery实现ajax或者用原生js写ajax都可以；
2. 服务端根据课程选择对应的服务端语言即可（如python web专业要求采用python+django）；
3. 数据库用sqlite3即可；
4. 检索的数据都存在数据库里面，通过ajax请求，访问到服务端的接口把数据以json格式返回并显示。具体效果参照百度搜索时的效果。


## 初步想法ajax_search
    使用ajax实现百度搜索自动补全的功能
    1.使用jquery实时捕获用户输入
    2.使用ajax向后台提交请求
    3.后台进行数据库查询,结果以json格式返回
    4.查询结果以查询次数排序(这小功能没有实现)
    5.数据库类似汉语词典

# 具体实现
## 检查数据库配置和创建modules并同步数据库
- 基于这次的索搜功能,设计的搜索数据库代码如下，基于sqlite3的数据库，不需要修改配置

```python
class Cnword(models.Model):
    # 词,解释,全拼
    words = models.CharField(max_length=255, blank=True)
    explain = models.TextField()
    py = models.CharField(max_length=255)
    searchcount = models.IntegerField(default=0, verbose_name='查询次数')

    class Meta:
        db_table = 'cnword'
        ordering = ('-searchcount',)  # 按照查询次数排序
    def __unicode__(self):
        return self.words
```

- 生成数据库的方法如下

```
python manage.py makemigrations search
python manage.py migrate

接下来就导入数据（使用软件导入）
```


- 遇到的问题,app没有注册，导致有modules同步也会报错
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'search',
]

##  创建搜索数据库的主页，并启动项目

- 先把url设置到对应的app下面（方法类似）

```
# django_homework项目下的urls.py配置
from django.conf.urls import include

urlpatterns = [
    url(r'^', include('todolist.urls')),
]
# todolist这个app下的urls.py配置
from todolist import views
urlpatterns = [
    url(r'^todolist/$', views.todolist, name='todolist'),
]

# todolist这个app下面views.py配置
def todolist(request):
    return render(request, 'todolist.html')
```

## 遇到的问题，找不到static
```
{% load staticfiles %}
<head lang="en">
    <meta charset="UTF-8">
    <title>搜索引擎</title>
    <script type="text/javascript" src="{% static 'js/jquery.min.js' %}"></script>
    <script type="text/javascript" src="{% static 'js/bootstrap.min.js' %}"></script>
    <link rel="stylesheet" href="{% static 'css/bootstrap.css' %}">
    <script type="text/javascript" src="{% static 'js/word.js' %}"></script>

</head>
```

## 先设计前段页面，这里我是用的是Bootstrap

```
<div class="container">
    <div class="row clearfix">
        <div class="col-md-4 column">
        </div>
        <div class="col-md-4 column">
            <h1 class="text-center text-danger">简单中文词语搜索引擎</h1>
            <div class="col-xs-6 col-md-8">
                <input id="input_search" type="text" class="form-control" size="30" placeholder="系统局限,仅支持中文搜索">
            </div>
            <div class="col-xs-6 col-md-4">
                <button type="button" class="btn btn-default btn-block" id="button_search">查询</button>
            </div>
            <div class="col-xs-6 col-md-8">
                <ul class="list-unstyled thumbnail" style="display: none" id="ul_search">
                </ul>
            </div>
        </div>

        <div class="col-md-4 column">
        </div>
    </div>
    <div class="row clearfix">
        <div class="col-md-2 column">
        </div>
        <div class="col-md-8 column">
            <p class="text-center thumbnail" style="display: none" id="p_search"></p>
        </div>
        <div class="col-md-2 column">
        </div>
    </div>
</div>
```

## 结合JQ,先实现前端部分的动作
```
$(document).ready(function () {
    var input_box = $('#input_search');//输入框input
    var ul = $('#ul_search');//待选列表ul
    var btn = $('#button_search');//按钮button
    var p = $('#p_search');//解释文本框p
    // 输入框得到焦点后 显示待选列表
    input_box.on('input propertychange', function () {
        p.hide();
        ul.show();
        kw = $.trim($(this).val())
        $.ajax({
            type: 'GET',
            url: '/search?kw=' + kw,
            dataType: 'json',
            success: function (result) {
                ul.empty();
                if (result.length > 0) {
                    $.each(result, function (i, item) {
                        var li_ = $('<li>' + item['words'] + '</li>').appendTo(ul);
                    })
                } else {
                    ul.empty();
                    $('<li>' + '没有这个词' + '</li>').appendTo(ul);
                }
            }
        })
    });
    // 输入框失去焦点后 隐藏待选列表
    input_box.blur(function () {
        ul.hide();
    });
    //待选列表鼠标滑入划出
    ul.on('mouseenter', 'li', (function () {
        $(this).css("background-color", "#F5F5F5");
        input_box.val($(this).text());//鼠标滑到那个待选词就把这个词放在输入框
    }));
    ul.on('mouseleave', 'li', (function () {
        $(this).css("background-color", "#ffffff");
    }));

    btn.on('click', function () {
        p.show()
    });
});   
```

## 最后是views和ajax之间的交互
> 这里也不是很难，主要就是知道前端和后端的数据格式，合理使用即可


### 搜索
```python
# 输入内容简单搜索
def search(request):
    # 获取Ajax POST过来的kw的数据
    kw = request.GET.get('kw')
    # 从数据库中查询出10条记录【QuerySet对象】
    word = Cnword.objects.filter(words__startswith=kw).values('words')[0:10]
    word = list(word)  # ValuesQuerySet对象需要先转换成list
    data = json.dumps(word)  # 把list转成json
    return HttpResponse(data)  # 返回json
```

```jquery
// 输入框得到焦点后 显示待选列表
input_box.on('input propertychange', function () {
    p.hide();
    ul.show();
    kw = $.trim($(this).val())
    $.ajax({
        type: 'GET',
        url: '/search?kw=' + kw,
        dataType: 'json',
        success: function (result) {
            ul.empty();
            if (result.length > 0) {
                $.each(result, function (i, item) {
                    var li_ = $('<li>' + item['words'] + '</li>').appendTo(ul);
                })
            } else {
                ul.empty();
                $('<li>' + '没有这个词' + '</li>').appendTo(ul);
            }
        }
    })
});
```

### 查询

```python
# 显示词条的具体搜索
def match(request):
    str_kw = request.GET.get('kw')
    unicode_kw = str_kw.encode()
    word = Cnword.objects.filter(words=unicode_kw).values('explain')
    word = list(word)
    data = json.dumps(word)
    return HttpResponse(data)
```

```jquery
// 查询按钮
    btn.on('click', function () {
        $.ajax({
            type: 'GET',
            url: '/match?kw=' + kw,
            dataType: 'json',
            success: function (result) {
                if (result) {
                    console.log(result)
                    p.empty();
                    p.text(result[0]['explain']);
                    p.show();
                } else {
                    p.empty();
                    p.text('没有解释');
                    p.show();
                }
            },
        })
    })
    
```

# 总结
- 这次作业虽然是ajax的,但是结合了Bootstrp让界面稍微好看一些
- JQ的语法有些已经忘记,需要去找有点麻烦(欠下来的总是要还的)