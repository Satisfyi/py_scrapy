import re
import requests
from DrissionPage import ChromiumPage
import time
import random
from bs4 import BeautifulSoup
import datetime
# from openpyxl import Workbook
import pymysql

conn=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='zhihu',
    charset='utf8mb4',
)
cursor=conn.cursor()
cursor.execute("""
               create table if not exists zhihu_hot_list
               (
                   id       int primary key auto_increment,
                   `rank`   int,
                   title    varchar(255),
                   main_content text,
                   hot     varchar(255),
                   name  varchar(255),
                   content text   ,
                   approve_save_comment  varchar(255),
                   time datetime
               )

               """)
print("数据库连接成功，表创建成功")
headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
         "cookie":"_xsrf=h6ctM5n2j8lPyimLVQGjcAoa7xVjIjDK; __zse_ck=005_NjzjjvjS8Ag3XvEKz0bJZJWK0BIrjV0vuXAwuqL5f6TrvGF1oV1rIDb5p05v/Az8qIkJhdmDKMD1ZfKIGZ1nse8d530XcMiy9oy0pQQKaoZtvVQbmz6zEb5al94XVXCF-ePqeEvnwiA07bzyQr6meIZ1yypwvY+DIvyoXA+Y3kxMhKpJOQUPotb96dOxMHVHPQizk/VUBZPlQHi7QejkK57PQ2neH7AS4MOJ/NYdU4vm8oJ8MAhnMYpVZ6o0D2kV8; _zap=f36fc1fc-c94a-4717-82ca-dcec691e1b24; d_c0=n_dXhaKEmxyPTpDM7QYQRJyTVUbre-D2akc=|1784252980; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1784252976; HMACCOUNT=A545A7F99E319E92; DATE=1784252977328; "
                  "crystal=U2FsdGVkX19kMwYeZ+bHV6HhQoocrcvfTG+NyI2seyy/mHPVVDS29TDcomDCsGDy3naYcFI4Pbo82xKqzM03cGA0fkjfRPohrCo2KNZszky18rhMhkEo1WH8jpDpQWGL4uJSRBWcL/Tge423iblPmmRNcxC3SlrZHKj/XxnctyPJ9YMfWQy1+dkE1vs+ilLZHyDwl0Vt2UHBuYq2J4KvCBWLny3dA0h1CMqXOA5drWizWbIsZ4ViETt9MBd69Mnw; cmci9xde=U2FsdGVkX1+g4TJ7tdTfm3JXO8Vd8I2j9zSZHY67rzcOHg5GHtsaGgZFt6M+rcZzcVU3FOYixkU8dKvqN448/g==; pmck9xge=U2FsdGVkX19We14anJViZcSd5kf+h76spZ5LvYprO0Q=; assva6=U2FsdGVkX1++7RR+O5N7I1KTgYCB0SEzsHSNc6tB310=; assva5=U2FsdGVkX1/HO+bJldQm4QnodArkAm"
                  "S18NKQIi9AGvhDtzmijpTigKnIg3C5AJAzOrVW19yKOSHBn3sGT4Jbwg==; vmce9xdq=U2FsdGVkX18tWloFUOCNKd7Roo1NmLnXYch1O347YsFLWKrZxLFkWCqL2aJD7qJsSl5tAw0mnLYdoSOGsXrInQoUmXq1XDjdtitN/e2uPFnK91kQGDrMstcAngHVnkM8UaORZpoz/Sj7zhfcb1aIPV7oVGBwePP0Op4shShP4pw=; gdxidpyhxdE=mvxf5%5CuI3O01Jebh54gb7%2FCc%5C4jooQGWRyviNY0PPe9G67lmD3E1HM9JdZKKyICde984%5CJXp4m%2FQ%5C%2FYTfsC%2Blv%5C3UkTH%2B5vGqzYpfJf24mDqCBOlDcy%2FfC7NnI%2Bgp1v4IwJ%2FZS5JJ4RC00wx2a7tHhOIR4JvH87SZjWWhvrKCkkdE%2FvW%3A1784253879696; captcha_session_v2=2|1:0|10:1784253039|18:captcha_session_v2|88:"
                  "aURWQW5oRjh3dXpMNVlQZ1AzdTNlcml6UGtDMWNrN0JqamxId0ZGd0NqTEJpcjcrbHBTdVlrU1pOQWRPWlVoNQ==|3db0655a7f13fcc1a6585e6b580b180312aedf2aeb2338fa9ddbedeae5853cea; captcha_ticket_v2=2|1:0|10:1784253073|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfZzNfYWNJbW5QbkpiZldhXyo5bXJQeFhDUGFRVVFfVkI2RHZwSHZZd3V2ZW1LYzlsZFhHcE55NFl3WCp2TyouaUFkUlRmUkpWd0NkWWFFVHRRc2lNdlVWRmpVNmp0eUVqcmxBME9tcS5neEdYcDhHQm9JLjJzMiowMGc5THRVVVZPM1hWUGtJNDEqTzJiRlZ4R2NfSjhuKktnaEoxMG5rM19FSmU1NmZaWWJ6Q0RaNmZMeTZDTy5qWDJCVHdETXd1ZWIxMlF5bEdnbUpWVUFnUTZfUWlmVy5nS1lOZE0yQXU4U0s0VWc"
                  "2eENKaGlyb2JfSG14UUhDMXV2NFVISDQ5ZVRPSGdzOXdHdThfMWd5VXFNbUE5WlBMNThzeHB3X21lR1ROUTRwbWlVZHdBdjN3XzUwRFU1ZTl6bTIuOHYwMWdaV0tGbGVzbW5scVA5RC5QSFJ3SkFkOFZLdlEqZi5EUFNycUJxaVM2ZURENlpYeVR0Wm5QeVJNUTk1Z2VIR2JrNmRQMWhZbldqWmVlakxlamRVTWEqU2xxY0JqWmlDd0xFKnB5S0xtdk0qejVXc3JaM0lHQmlycUFrMkRFQXpyRW1PMXZVZUUyeUNZRHlIT1hpWXNpeWpocmVTLlJ6U3h1TGpaaWVITE1zdjBsZkN5TDBLVjJnVldNX0pfU2tIOTVvNXZ4dGc3N192X2lfMSJ9|f01a70c6e60ae5180d5ba4992da40a620dfe6eeb3855bd98c03dbe417df99d47; q_c1=efcc05fcecc54322971ff09637c9060c|1784267628000|1784267628000; z_c0=2|1:0|10:1784267630|"
                  "4:z_c0|92:Mi4xSEtjd2RBWUFBQUNmOTFlRm9vU2JIQ1lBQUFCZ0FsVk5vZGhHYXdDZzVBRVJoemY0emhpYnA5QlpqMFFoQU1OQ193|de9c5911410c186f6964b4fd82f96bc99b7835da09565f709ea13658ae382d3d; SESSIONID=qg9Pj6ty2237wDc61PvcmQM1CFLjFRvd2wg3RvUE7rM; JOID=VlEUAE3a11f2h3M0WLBOiwAk8KBBprhso-9ISCPq6GzD9TVaZrEeCZuIdj5fwF5sn4X-_xXvkiX_TyNsEI6YOdE=; osd=U1gVBE7f3lbyhHY9WbRNjgkl9KNEr7looOpBSSfp7WXC8TZfb7AaCp6BdzpcxVdtm4b79hTrkSD2TidvFYeZPdI=; BEC=04678b89b8500afc30b012aad143c9b0; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1784267648"}
url="https://www.zhihu.com/hot"
#模拟真实请求
def sleep_time():
    time.sleep(random.randint(1,3))

#数据清洗
def clean_data(text):
    return re.sub(r'\s+',' ',text).strip()

#数据去标签
def html_to_text(html):
    return clean_data(BeautifulSoup(html,'lxml').get_text(" "))

#改为标准时间
def time_trans(ts):

    dt=datetime.datetime.fromtimestamp(
        ts,tz=datetime.timezone(datetime.timedelta(hours=8))
    )
    return dt.strftime("%Y-%m-%d %H:%M:%S")

#解析静态页面
def parse_static_data():
    # 拿静态页面直接用requests
    print("开始爬取静态页面")
    try:
        res = requests.get(headers=headers, url=url)
        response = res.text
    except Exception as e:
        print(f"请求失败: {e}")
        return []
    # print(response.text)
    soup = BeautifulSoup(response, 'lxml')
    items = soup.find_all('section', class_="HotItem")
    hot_list=[]
    # 第一次遍历，获得静态标题，热度
    for index, item in enumerate(items):
        try:
            title = item.find('h2').get_text()
            main_content = item.find('p', class_='HotItem-excerpt').get_text()if item.find('p', class_='HotItem-excerpt')else ''
            hot = item.find('div', class_="HotItem-metrics HotItem-metrics--bottom").get_text().split('分')[0].replace('\u200b','').strip()if item.find('div', class_="HotItem-metrics HotItem-metrics--bottom")else ''
            # print(f"排名{index+1}. {title}")
            id = item.find('a').attrs['href'].split('/')[-1].split('?')[0]
            hot_list.append({"排名":index+1,"标题":title,"内容":main_content,'热度':hot,"id":id})
        except Exception as e:
            print(f"解析静态页面出错: {e}")
            continue
        sleep_time()
        print(f"静态页面解析完成，共{len(hot_list)}条数据")
    return hot_list


#解析动态问答页面
def parse_answer_data(tab,item):
    id=item['id']
    results=[]
    tab.listen.start(f'api/v4/questions/{id}/feeds')
    sleep_time()
    tab.get(f'https://www.zhihu.com/question/{id}')
    tab.scroll.to_bottom()
    sleep_time()

    for _ in range(5):
        r = tab.listen.wait(timeout=5)

        if not r:
            break

        json_data = r.response.body

        if not isinstance(json_data, dict) or 'data' not in json_data:
            continue

        data_list = json_data["data"]

        for data in data_list:
            try:
                name = data['target']['author']['name']if data['target']['author']else ''
                content = html_to_text(data['target']['content'])
                # print(content)
                approve_save_comment = data['target']['matrix_tips']
                time_original = data['target']['created_time']
                time = time_trans(time_original)
                dic = {"排名":item['排名'],"标题":item['标题'],"内容":item['内容'],'热度':item['热度'],'用户': name, "评论内容": content, "点赞-收藏-评论": approve_save_comment, '发布时间': time}
                print(dic)
                results.append(dic)
            except Exception as e:
                print(f"解析问答页面出错: {e}，标题为{item['标题']}")
                continue
            sleep_time()

    return results


# wb = Workbook()
# # ws = wb.active
# ws.append(['排名', '标题', '内容', '热度', '用户', '评论内容', '点赞-收藏-评论', '发布时间'])
def save_data(item):
    cursor.execute("""insert into zhihu_hot_list(`rank`, title, main_content, hot, name, content, approve_save_comment, time) values(%s, %s, %s, %s, %s, %s, %s, %s)""",(item['排名'],item['标题'],item['内容'],item['热度'],item['用户'],item['评论内容'],item['点赞-收藏-评论'],item['发布时间']))
    sleep_time()
    conn.commit()
    # ws.append([item['排名'],item['标题'],item['内容'],item['热度'],item['用户'],item['评论内容'],item['点赞-收藏-评论'],item['发布时间']])


def main():
    hot_list=parse_static_data()
    co=ChromiumPage()
    tab=co.latest_tab
    for item in hot_list:
        try:
            dics=parse_answer_data(tab,item)
            for dic in dics:
                save_data(dic)
        except Exception as e:
            print(f"出错: {e}，标题为{item['标题']}")
            continue
    print("数据已保存到数据库")
    cursor.close()
    conn.close()
    # wb.save('知乎热榜.xlsx')
    # print(f'数据已保存到知乎热榜.xlsx')

if __name__ == '__main__':
    main()
