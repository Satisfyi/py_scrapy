"""
数据库模型 —— 定义了「知乎热榜话题」和「知乎评论」两张表

理解方式：这个类就像 Excel 表格的表头
    - 每个字段 = 一列
    - 每一行数据 = 一条记录

当 Django 执行 migrate 后，会自动在数据库中建表。
"""

from django.db import models



class Topic(models.Model):
    """知乎热榜话题"""

    # ---- 基础信息 ----
    content_id = models.CharField(
        max_length=255,
        unique=True,                # 知乎问题/回答的唯一ID，用于去重
        default='',                 # 默认空字符串，方便迁移已有数据
        verbose_name='内容ID'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='标题'
    )

    main_content = models.TextField(
        blank=True,                 # 允许为空
        default='',
        verbose_name='主要内容'
    )

    url = models.URLField(
        max_length=500,
        verbose_name='知乎链接'
    )

    hot_value = models.IntegerField(
        default=0,
        verbose_name='热度值'
    )

    rank = models.IntegerField(
        verbose_name='排名',
    )

    # ---- 时间 ----
    create_time = models.DateTimeField(
        auto_now=True,          # 每次更新都刷新时间，保证过滤当天数据时能匹配到
        verbose_name='入库时间'
    )

    # ---- 表设置 ----
    class Meta:
        db_table = 'topic'         # 与爬虫原表名保持一致
        verbose_name = '知乎热榜'
        verbose_name_plural = verbose_name
        ordering = ['-hot_value']

    def __str__(self):
        return f'第{self.rank}名: {self.title}'


class Comment(models.Model):
    """知乎评论/回答"""

    # ---- 关联 ----
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,           # 话题删除时，关联评论也删除
        related_name='comments',            # 可以通过 topic.comments 访问
        verbose_name='所属话题',
        null=True,
        blank=True
    )

    content_id = models.CharField(
        max_length=255,
        verbose_name='内容ID',
        db_index=True                       # 加索引，查询更快
    )

    # ---- 评论信息 ----
    name = models.CharField(
        max_length=255,
        default='',
        verbose_name='用户名'
    )

    content = models.TextField(
        blank=True,
        default='',
        verbose_name='评论内容'
    )

    approve_save_comment = models.CharField(
        max_length=255,
        default='',
        verbose_name='点赞-收藏-评论'
    )

    time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='发布时间'
    )

    # ---- 表设置 ----
    class Meta:
        db_table ='zhihu_comment'          # 与爬虫原表名保持一致
        verbose_name = '知乎评论'
        verbose_name_plural = verbose_name
        ordering = ['-time']                # 按时间倒序，最新在前

    def __str__(self):
        return f'{self.name}: {self.content[:30]}'
