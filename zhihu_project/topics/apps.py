"""
告诉 Django 这个 app 叫什么名字，启动时自动开启定时调度
"""
import os
from django.apps import AppConfig


class TopicsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'topics'
    verbose_name = '知乎热榜'

    def ready(self):
        # 防止 runserver 自动重载导致调度器重复启动
        if os.environ.get('RUN_MAIN') != 'true':
            return
        from .scheduler import start_scheduler
        start_scheduler()
