"""
topics 应用的路由

路由的作用就像是「电话总机」：
    用户拨什么号码（访问什么网址）→ 转接到对应的接线员（views 函数）

例如：
    访问 /        → 调用 index 视图函数
    访问 /admin/  → 调用 Django 后台
"""

from django.urls import path
from . import views

urlpatterns = [
    # path('网址路径', 视图函数, name='别名')
    # '' 表示根路径，也就是 http://127.0.0.1:8000/
    path('', views.index, name='index'),
]
