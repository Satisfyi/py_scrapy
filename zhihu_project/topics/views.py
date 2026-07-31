"""
视图（views）—— 处理网页请求，返回网页内容

通俗理解：
    用户在浏览器输入网址 → Django 找到对应的 views → views 返回 HTML 页面

这里的 index() 函数就是处理首页请求的：
    1. 从数据库读取所有热榜数据
    2. 把数据传给 HTML 模板
    3. 返回一个完整的网页
"""

from django.shortcuts import render
from .models import Topic
from django.utils import timezone
import datetime

def index(request):
    """
    首页：展示知乎热榜列表

    request 是 Django 自动传入的请求对象，
    里面包含了用户的信息（谁访问的、用什么浏览器等）
    """

    # 获取北京时间的今天 00:00 和明天 00:00（UTC 时间）
    now = timezone.now()  # 北京时间
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow_start = today_start + datetime.timedelta(days=1)

    # 只显示当天爬取的数据，按热度降序排列
    topic_list = Topic.objects.filter(
        create_time__gte=today_start,#创建时间大于today_start，假设now变量为2026-7-20，下午两点，today_start就是7-20，0：00，tomorrow_start就是7-21 0：00
        create_time__lt=tomorrow_start#创建时间小于tomorrow_start
    ).order_by('-hot_value')
    # render() 做三件事：
    #   1. 找到 templates/index.html 这个模板文件
    #   2. 把 topic_list 数据传给模板
    #   3. 拼接成完整的 HTML 返回给浏览器
    return render(request, 'index.html', {
        'topics': topic_list
    })
