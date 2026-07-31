import os
import sys
import re
import requests
from DrissionPage import ChromiumPage
import time
import random
from bs4 import BeautifulSoup
import datetime
import logging

#设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('zhihu_crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ZhihuSpider:

    # 伪装请求头
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        "cookie": "_xsrf=h6ctM5n2j8lPyimLVQGjcAoa7xVjIjDK; __zse_ck=005_NjzjjvjS8Ag3XvEKz0bJZJWK0BIrjV0vuXAwuqL5f6TrvGF1oV1rIDb5p05v/Az8qIkJhdmDKMD1ZfKIGZ1nse8d530XcMiy9oy0pQQKaoZtvVQbmz6zEb5al94XVXCF-ePqeEvnwiA07bzyQr6meIZ1yypwvY+DIvyoXA+Y3kxMhKpJOQUPotb96dOxMHVHPQizk/VUBZPlQHi7QejkK57PQ2neH7AS4MOJ/NYdU4vm8oJ8MAhnMYpVZ6o0D2kV8; _zap=f36fc1fc-c94a-4717-82ca-dcec691e1b24; d_c0=n_dXhaKEmxyPTpDM7QYQRJyTVUbre-D2akc=|1784252980; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1784252976; HMACCOUNT=A545A7F99E319E92; DATE=1784252977328; "
                  "crystal=U2FsdGVkX19kMwYeZ+bHV6HhQoocrcvfTG+NyI2seyy/mHPVVDS29TDcomDCsGDy3naYcFI4Pbo82xKqzM03cGA0fkjfRPohrCo2KNZszky18rhMhkEo1WH8jpDpQWGL4uJSRBWcL/Tge423iblPmmRNcxC3SlrZHKj/XxnctyPJ9YMfWQy1+dkE1vs+ilLZHyDwl0Vt2UHBuYq2J4KvCBWLny3dA0h1CMqXOA5drWizWbIsZ4ViETt9MBd69Mnw; cmci9xde=U2FsdGVkX1+g4TJ7tdTfm3JXO8Vd8I2j9zSZHY67rzcOHg5GHtsaGgZFt6M+rcZzcVU3FOYixkU8dKvqN448/g==; pmck9xge=U2FsdGVkX19We14anJViZcSd5kf+h76spZ5LvYprO0Q=; assva6=U2FsdGVkX1++7RR+O5N7I1KTgYCB0SEzsHSNc6tB310=; assva5=U2FsdGVkX1/HO+bJldQm4QnodArkAm"
                  "S18NKQIi9AGvhDtzmijpTigKnIg3C5AJAzOrVW19yKOSHBn3sGT4Jbwg==; vmce9xdq=U2FsdGVkX18tWloFUOCNKd7Roo1NmLnXYch1O347YsFLWKrZxLFkWCqL2aJD7qJsSl5tAw0mnLYdoSOGsXrInQoUmXq1XDjdtitN/e2uPFnK91kQGDrMstcAngHVnkM8UaORZpoz/Sj7zhfcb1aIPV7oVGBwePP0Op4shShP4pw=; gdxidpyhxdE=mvxf5%5CuI3O01Jebh54gb7%2FCc%5C4jooQGWRyviNY0PPe9G67lmD3E1HM9JdZKKyICde984%5CJXp4m%2FQ%5C%2FYTfsC%2Blv%5C3UkTH%2B5vGqzYpfJf24mDqCBOlDcy%2FfC7NnI%2Bgp1v4IwJ%2FZS5JJ4RC00wx2a7tHhOIR4JvH87SZjWWhvrKCkkdE%2FvW%3A1784253879696; captcha_session_v2=2|1:0|10:1784253039|18:captcha_session_v2|88:"
                  "aURWQW5oRjh3dXpMNVlQZ1AzdTNlcml6UGtDMWNrN0JqamxId0ZGd0NqTEJpcjcrbHBTdVlrU1pOQWRPWlVoNQ==|3db0655a7f13fcc1a6585e6b580b180312aedf2aeb2338fa9ddbedeae5853cea; captcha_ticket_v2=2|1:0|10:1784253073|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfZzNfYWNJbW5QbkpiZldhXyo5bXJQeFhDUGFRVVFfVkI2RHZwSHZZd3V2ZW1LYzlsZFhHcE55NFl3WCp2TyouaUFkUlRmUkpWd0NkWWFFVHRRc2lNdlVWRmpVNmp0eUVqcmxBME9tcS5neEdYcDhHQm9JLjJzMiowMGc5THRVVVZPM1hWUGtJNDEqTzJiRlZ4R2NfSjhuKktnaEoxMG5rM19FSmU1NmZaWWJ6Q0RaNmZMeTZDTy5qWDJCVHdETXd1ZWIxMlF5bEdnbUpWVUFnUTZfUWlmVy5nS1lOZE0yQXU4U0s0VWc"
                  "2eENKaGlyb2JfSG14UUhDMXV2NFVISDQ5ZVRPSGdzOXdHdThfMWd5VXFNbUE5WlBMNThzeHB3X21lR1ROUTRwbWlVZHdBdjN3XzUwRFU1ZTl6bTIuOHYwMWdaV0tGbGVzbW5scVA5RC5QSFJ3SkFkOFZLdlEqZi5EUFNycUJxaVM2ZURENlpYeVR0Wm5QeVJNUTk1Z2VIR2JrNmRQMWhZbldqWmVlakxlamRVTWEqU2xxY0JqWmlDd0xFKnB5S0xtdk0qejVXc3JaM0lHQmlycUFrMkRFQXpyRW1PMXZVZUUyeUNZRHlIT1hpWXNpeWpocmVTLlJ6U3h1TGpaaWVITE1zdjBsZkN5TDBLVjJnVldNX0pfU2tIOTVvNXZ4dGc3N192X2lfMSJ9|f01a70c6e60ae5180d5ba4992da40a620dfe6eeb3855bd98c03dbe417df99d47; q_c1=efcc05fcecc54322971ff09637c9060c|1784267628000|1784267628000; z_c0=2|1:0|10:1784267630|"
                  "4:z_c0|92:Mi4xSEtjd2RBWUFBQUNmOTFlRm9vU2JIQ1lBQUFCZ0FsVk5vZGhHYXdDZzVBRVJoemY0emhpYnA5QlpqMFFoQU1OQ193|de9c5911410c186f6964b4fd82f96bc99b7835da09565f709ea13658ae382d3d; SESSIONID=qg9Pj6ty2237wDc61PvcmQM1CFLjFRvd2wg3RvUE7rM; JOID=VlEUAE3a11f2h3M0WLBOiwAk8KBBprhso-9ISCPq6GzD9TVaZrEeCZuIdj5fwF5sn4X-_xXvkiX_TyNsEI6YOdE=; osd=U1gVBE7f3lbyhHY9WbRNjgkl9KNEr7looOpBSSfp7WXC8TZfb7AaCp6BdzpcxVdtm4b79hTrkSD2TidvFYeZPdI=; BEC=04678b89b8500afc30b012aad143c9b0; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1784267648"
    }

    target_url = "https://www.zhihu.com/hot"

    def __init__(self):
        #初始化：启动浏览器（数据库由 Django ORM 管理，无需手动连接）
        self.browser = ChromiumPage()
        self.tab = self.browser.latest_tab
        logger.info("Django ORM 已就绪，浏览器启动成功")

    @staticmethod
    def time_sleep():
        #模拟真实请求间隔
        time.sleep(random.randint(1, 3))

    @staticmethod
    def clean_text(text):
        #数据清洗：合并多余空白
        return re.sub(r'\s+', ' ', text).strip()

    @classmethod
    def html_to_text(cls, html):
        #HTML 去标签，提取纯文本
        return cls.clean_text(BeautifulSoup(html, 'lxml').get_text(" "))

    @staticmethod
    def timestamp_to_dt(ts):
        """将时间戳转换为带时区的 datetime 对象（东八区）"""
        return datetime.datetime.fromtimestamp(
            ts, tz=datetime.timezone(datetime.timedelta(hours=8))
        )

    @staticmethod
    def parse_hot_value(text):
        text = text.replace('\u200b', '').strip()
        # 只提取数字部分，不乘任何倍数
        match = re.search(r'([\d.]+)', text)
        if not match:
            return 0
        return int(float(match.group(1)))


    def parse_static_page(self):
        #解析知乎热榜静态页面，获取热榜列表
        logger.info("开始爬取静态页面")
        try:
            res = requests.get(headers=self.headers, url=self.target_url)
            response = res.text
        except Exception as e:
            logger.error(f"请求失败: {e}")
            return []

        soup = BeautifulSoup(response, 'lxml')
        items = soup.find_all('section', class_="HotItem")
        hot_list = []

        for index, item in enumerate(items):
            try:
                title = item.find('h2').get_text()
                main_content = item.find('p', class_='HotItem-excerpt').get_text() if item.find('p', class_='HotItem-excerpt') else ''
                hot_text = item.find('div', class_="HotItem-metrics HotItem-metrics--bottom").get_text() if item.find('div', class_="HotItem-metrics HotItem-metrics--bottom") else ''
                if not hot_text:
                    logger.warning(f"未获取到热度值，跳过: {title}")
                    continue
                hot = self.parse_hot_value(hot_text)
                content_id = item.find('a').attrs['href'].split('/')[-1].split('?')[0]
                hot_list.append({
                    "排名": index + 1,
                    "标题": title,
                    "内容": main_content,
                    '热度': hot,
                    "content_id": content_id
                })
            except Exception as e:
                logger.warning(f"解析静态页面出错: {e}")
                continue
            self.time_sleep()

        logger.info(f"静态页面解析完成，共{len(hot_list)}条数据")
        return hot_list

    def parse_answers(self, item):
        #解析单个热榜问题的动态问答数据
        content_id = item['content_id']
        results = []

        self.tab.listen.start(f'api/v4/questions/{content_id}/feeds')
        self.time_sleep()
        self.tab.get(f'https://www.zhihu.com/question/{content_id}')
        self.tab.scroll.to_bottom()
        self.time_sleep()

        for _ in range(5):
            r = self.tab.listen.wait(timeout=7)
            if not r:
                break

            json_data = r.response.body
            if not isinstance(json_data, dict) or 'data' not in json_data:
                continue

            data_list = json_data["data"]
            for data in data_list:
                try:
                    name = data['target']['author']['name'] if data['target']['author'] else ''
                    content = self.html_to_text(data['target']['content'])
                    approve_save_comment = data['target']['matrix_tips']
                    time_original = data['target']['created_time']
                    time_dt = self.timestamp_to_dt(time_original)
                    dic = {
                        "content_id":content_id,
                        '用户': name,
                        "评论内容": content,
                        "点赞-收藏-评论": approve_save_comment,
                        '发布时间': time_dt
                    }
                    # logger.info(f"[{item['排名']}] {item['标题']} | 评论:{content[:50]}... | {time_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    results.append(dic)
                except Exception as e:
                    logger.warning(f"解析问答页面出错: {e}，标题为{item['标题']}")
                    continue
                self.time_sleep()

        return results

    def save_static_to_db(self, item):
        #将单条热榜数据写入数据库（使用 Django ORM）
        from topics.models import Topic
        topic, created = Topic.objects.update_or_create(
            # 查找条件
            content_id=item['content_id'],
            #会更新
            defaults={
                'rank': item['排名'],
                'title': item['标题'],
                'main_content': item['内容'],
                'hot_value': item['热度'],
                'url': f"https://www.zhihu.com/question/{item['content_id']}",
            }
        )
        if created:
            logger.info(f"新增热榜: [{item['排名']}] {item['标题']}")
        else:
            logger.info(f"更新热榜: [{item['排名']}] {item['标题']}")

    def save_comment_to_data(self, answer):
        #将单条评论数据写入数据库（使用 Django ORM）
        # 给评论找到它所属的话题
        from topics.models import Topic, Comment
        try:
            topic = Topic.objects.get(content_id=answer['content_id'])
        except Topic.DoesNotExist:
            topic = None

        Comment.objects.create(
            topic=topic,
            content_id=answer['content_id'],
            name=answer['用户'],
            content=answer['评论内容'],
            approve_save_comment=answer['点赞-收藏-评论'],
            time=answer['发布时间'],
        )
        self.time_sleep()

    def run(self):
        #执行完整爬取流程
        hot_list = self.parse_static_page()
        for item in hot_list:
            try:
                self.save_static_to_db(item)
                answer_list = self.parse_answers(item)
                for answer in answer_list:
                    self.save_comment_to_data(answer)
            except Exception as e:
                logger.error(f"出错: {e}，标题为{item['标题']}")
                continue
        logger.info("数据已保存到数据库")

    def close(self):
        #释放资源（Django ORM 会自动管理连接，无需手动关闭）
        logger.info("爬取完成，资源已释放")


if __name__ == '__main__':
    # Django 环境初始化（仅在独立运行时需要）
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhihu_project.settings')
    import django
    django.setup()

    spider = ZhihuSpider()
    try:
        spider.run()
    finally:
        spider.close()
