"""
APScheduler 定时调度：每天自动爬取知乎热榜
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from spider.scrapy_link_django import ZhihuSpider

logger = logging.getLogger('topics.scheduler')

scheduler = BackgroundScheduler()


def crawl_job():
    """定时任务：执行爬虫"""
    spider = ZhihuSpider()
    try:
        spider.run()
        logger.info("定时爬取完成")
    finally:
        spider.close()


def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        crawl_job,
        trigger=CronTrigger(hour=10, minute=0),
        id='daily_crawl',
        name='每日知乎热榜爬取',
        replace_existing=True,
    )
    scheduler.start()
    logger.info("定时调度器已启动，每天 17:00 执行爬取")


def stop_scheduler():
    """关闭调度器"""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("定时调度器已关闭")
