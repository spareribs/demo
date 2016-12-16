/**
 * Created by Spareribs on 2016/12/14.
 * 需要处理的事件有：
 * 1. 输入框失去焦点后 隐藏待选列表
 * 2. 输入框获得焦点, 如果有内容就显示待选列表
 * 3. 待选列表鼠标滑入划出
 */


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
    // 查询隐藏解析列表
    btn.on('click', function () {
        p.show()
    });

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
});