/**
 * Created by Spareribs on 2016/11/28.
 */

// delete button按钮的ajax
$(document).on('click', ".delete", function () {
    this_button = $(this)
    rowid = this_button.attr('data-id')
    console.log(this_button, rowid)
    $.ajax({
        type: 'POST',
        url: '/del_todolist?rowid=' + rowid,
        dataType: 'json',
        success: function (result) {
            console.log(result)
            console.log(this_button)
            this_button.closest('li').remove()
        }
    })
})

// 点击edit后显示修改提交的form
$(document).on('click', ".edit", function () {
    $(this).closest('li').find('form').css('display', 'block')
})

// 点击checkbox后显示修改提交的form
$(document).on('click', ".checkbox", function () {
	var $li =  $(this).closest('li')
	var rowid = $(this).closest('div').attr('data-id')
	var status = $li.hasClass("completed_item") ? '0':'1'
    console.log(rowid, status)
	$.ajax({
            type: 'POST',
            url: '/chk_todolist?rowid=' + rowid + '&status='+status,
            dataType: 'json',
            success: function (result) {
                console.log(result)
                $li.hasClass("completed_item") ? $li.removeClass("completed_item") : $li.addClass("completed_item")
            }
        })
})