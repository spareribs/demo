# coding: utf-8
# author: spareribs

from django import template
import time
import datetime
from dateutil.relativedelta import relativedelta

register = template.Library()


# 将 datetime obj 转换成 timestamp
def date_to_timestamp(date_time):
    return time.mktime(date_time.timetuple())


def time_before():
    timestamp_before = {
        # 1分钟前的时间戳
        'a_minute_before': '',
        # 1小时前的时间戳
        'a_hour_before': '',
        # 1天前的时间戳
        'a_day_before': '',
        # 1周前的时间戳
        'a_week_before': '',
        # 1个月的时间戳
        'a_month_before': '',
        # 1年的时间戳
        'a_year_before': '',
    }
    # 获取当前时间
    now = datetime.datetime.now()
    # 得到1个分钟前的时间（datetim obj）
    timestamp_before['a_minute_before'] = now + relativedelta(minutes=-1)
    # 得到1个小时前的时间（datetim obj）
    timestamp_before['a_hour_before'] = now + relativedelta(hours=-1)
    # 得到1天前的时间（datetim obj）
    timestamp_before['a_day_before'] = now + relativedelta(days=-1)
    # 得到1周前的时间（datetim obj）
    timestamp_before['a_week_before'] = now + relativedelta(weeks=-1)
    # 得到1个月前的时间（datetim obj）
    timestamp_before['a_month_before'] = now + relativedelta(months=-1)
    # 得到1年前的时间（datetim obj）
    timestamp_before['a_year_before'] = now + relativedelta(years=-1)
    # 将datetim obj转换成 timestamp
    for time_tag in timestamp_before:
        timestamp_before[time_tag] = date_to_timestamp(timestamp_before[time_tag])
    return timestamp_before


@register.filter()
def format_date(value):
    before = time_before()
    add_date = date_to_timestamp(value)
    if before['a_minute_before'] < add_date:
        print(before['a_minute_before'], add_date)
        time_ = int(61 - (add_date - before['a_minute_before']))
        return "{0}秒前发布".format(time_)

    elif before['a_hour_before'] < add_date:
        print(before['a_hour_before'], add_date)
        time_ = int(61 - (add_date - before['a_hour_before']) / 60)
        return "{0}分钟前发布".format(time_)

    elif before['a_day_before'] < add_date:
        print(before['a_day_before'], add_date)
        time_ = int(25 - (add_date - before['a_day_before']) / 3600)
        return "{0}小时前发布".format(time_)

    elif before['a_week_before'] < add_date:
        print(before['a_week_before'], add_date)
        time_ = int(8 - (add_date - before['a_week_before']) / 86400)
        return "{0}天前发布".format(time_)

    elif before['a_month_before'] < add_date:
        print(before['a_month_before'], add_date, before['a_month_before'])
        time_ = int(5 - (add_date - before['a_month_before']) / 604800)
        return "{0}周前发布".format(time_)

    elif before['a_year_before'] < add_date:
        print(before['a_year_before'], add_date)
        time_ = int(13 - (add_date - before['a_year_before']) / 2592000)
        return "{0}个月前发布".format(time_)
    else:
        print(before, add_date)
        return "1年前发布"
