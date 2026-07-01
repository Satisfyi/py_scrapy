import requests
import os.path
from bs4 import BeautifulSoup
import time
import random
from openpyxl import Workbook
wb=Workbook()
ws=wb.active
ws.append(['排名','电影名称','导演','年份','国家','评分','经典台词'])
#请求数据
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
    "Cookie":'ll="118254"; bid=odYOVyhuSLs; _pk_id.100001.4cf6=dd51bedc9106ef06.1774249526.;'
    ' __yadk_uid=DWq4eZcXCHNUzH1IC5v3MGvvzAgaNAtw; _vwo_uuid_v2=DA1F263C2E0646284A747FEB44EBDD480|cf97e3b424d95bde580da636f846b769;'
    ' _ga_Y4GN1R87RG=GS2.1.s1774263130$o2$g0$t1774263130$j60$l0$h0; _ga=GA1.1.743228199.1774249525;'
    ' _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1782706770%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D;'
    ' _pk_ses.100001.4cf6=1; __utma=30149280.743228199.1774249525.1774253954.1782706771.3;'
    ' __utmb=30149280.0.10.1782706771; __utmc=30149280; '
    '__utmz=30149280.1782706771.3.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/;'
    ' __utma=223695111.378357839.1774249525.1774253954.1782706771.3; __utmb=223695111.0.10.1782706771;'
    ' __utmc=223695111; __utmz=223695111.1782706771.3.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
}
page=0
i=1
k=1
while page<250:
    url=f'https://movie.douban.com/top250?start={page}&filter='
    page+=25
    data=requests.get(headers=headers,url=url)

    response=data.text

    # print(response)
    soup=BeautifulSoup(response,'lxml')

    items=soup.find_all('div',class_='item')
    # print(len(items))
    print(f'开始爬取第{i}页的数据，共{len(items)}条数据')
    for item in items:
        try:
            rank=k
            name=item.find('span',class_='title').get_text()
            bd_div=item.find('div',class_='bd')
            director=bd_div.find('p').get_text().strip().split(" ")[1]
            year=bd_div.find('p').get_text().strip().split("\n")[1].strip().split("/")[0].strip()
            country=bd_div.find('p').get_text().strip().split('\n')[1].strip().split('/')[1].strip()
            score=item.find('span',class_='rating_num').get_text()
            quote=item.find('p',class_='quote').get_text().strip()if item.find('p',class_='quote') else ''
            dic={'排名':rank,'电影名称：':name,'导演':director,'年份':year,'国家':country,'评分':score,'经典台词':quote}
            k+=1
            print(dic)
            #设置间隔
            time.sleep(random.randint(1,3))
            ws.append([rank,name,director,year,country,score,quote])
        except Exception as e:
            print(f'第{k}条数据爬取失败,错误信息:{e}')
            k+=1
            continue
    print(f'第{i}页数据爬取完成')
    print(f'数据已保存到{os.path.abspath("豆瓣电影TOP250.xlsx")}')
    i+=1
wb.save('豆瓣电影TOP250.xlsx')
