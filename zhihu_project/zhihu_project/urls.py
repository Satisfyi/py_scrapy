"""
项目主路由

每个 path() 就是一条「访问规则」：
    path('admin/', ...)   → 访问 /admin/ 会打开后台管理
    path('', ...)         → 访问 / 会显示知乎热榜首页
"""

from django.contrib import admin
from django.urls import path, include
#这是整个网站的总入口，Django收到请求后先到这里
urlpatterns = [
    path('admin/', admin.site.urls),         # Django 自带后台
    path('', include('topics.urls')),        # 首页 → 交给 topics 应用处理，转发——不再自己处理，把请求交给 topics/urls.py继续匹配
]
