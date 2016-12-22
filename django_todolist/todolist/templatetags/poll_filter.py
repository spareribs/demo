# coding: utf-8
# author: spareribs
from django import template
import datetime

register = template.Library()

@register.filter()
def time_before(d):
    chunks = (
        (60 * 60 * 24 * 365, u'年'),
        (60 * 60 * 24 * 30, u'月'),
        (60 * 60 * 24 * 7, u'周'),
        (60 * 60 * 24, u'天'),
        (60 * 60, u'小时'),
        (60, u'分钟'),
        (1, u'秒'),
    )

    # 如果不是datetime类型转换后与datetime比较
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    now = datetime.datetime.now()
    delta = now - d
    print(delta)
    # 忽略毫秒
    before = delta.days * 24 * 60 * 60 + delta.seconds
    # 刚刚过去的1分钟
    if before <= 3:
        return u'刚刚'
    for seconds, unit in chunks:
        count = before // seconds
        if count != 0:
            break
    return str(count) + str(unit) + u"前发布"