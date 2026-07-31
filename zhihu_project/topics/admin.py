"""
Djago Admin 配置 —— 让后台可以管理知乎热榜数据

注册了 Topic 后，进入 /admin/ 就能看到「知乎热榜」菜单
可以在这里：查看、搜索、删除数据
"""

from django.contrib import admin
from .models import Topic


@admin.register(Topic)      # 这行代码 = 把 Topic 表注册到后台
class TopicAdmin(admin.ModelAdmin):
    # 列表页显示的列
    list_display = ['rank', 'title', 'hot_value', 'url', 'create_time']

    # 可以搜索标题
    search_fields = ['title']

    # 右侧可以按排名筛选
    list_filter = ['rank']
