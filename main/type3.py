#适配于 笔趣阁(https://www.22shuqu.com) 该类网站



import re

import requests
from bs4 import BeautifulSoup
import time
import logging


# 配置日志记录器
logging.basicConfig(level=logging.DEBUG,  # 设置日志级别
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
                    datefmt='%Y-%m-%d %H:%M:%S')  # 设置日期和时间格式
logger = logging.getLogger(__name__)

def delete_text(content_text , unwanted_text):
    cleaned_text = content_text.replace(unwanted_text, "")
    return cleaned_text

def get(url , next_bool):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    head_div = soup.find('h1' , class_='title')
    head_text = head_div.get_text() if head_div else ''

    content_div = soup.find('div', id='content', class_='content' )

    # print(soup)
    # print(head_div)

    paragraphs = content_div.find_all('p')
    content_text = '\n'.join(p.get_text() for p in paragraphs)

    # print(content_text)


    unwanted_text = ["小主，这个章节后面还有哦^.^，请点击下一页继续阅读，后面更精彩！" , "这章没有结束^.^，请点击下一页继续阅读！" , "喜欢修真四万年请大家收藏：(m.shaonianshuwu.com)修真四万年少年书屋更新速度全网最快。","本小章还未完~.~，请点击下一页继续阅读后面精彩内容！"]
    for i in unwanted_text:
        content_text = delete_text(content_text, i)

    if next_bool == 1:
        content_text = "\n\n\n"+head_text+"\n"+content_text

    # 查找包含“下一页”文本的 <a> 标签
    next_page_tag = soup.find('a', id = 'next_url')

    nxt = 0

    # print(next_page_tag)

    # 提取并打印该标签的 href 属性
    if next_page_tag.get_text() == ' 下一页':
        next_page_href = next_page_tag['href']
    else:
        logger.info(head_text+" 已结束")
        # print(head_text+" 已结束")
        # next_page_tag = soup.find('a', text="下一章")
        next_page_href = next_page_tag['href']
        nxt = 1


    # print("Next page href:", next_page_href)
    return content_text , next_page_href , nxt


url = "https://www.22shuqu.com"
suffix = "/b/899/899830/252236360.html"   #需要添加的书籍，第一章url
nxt = 1

for i in range(1500):
    content_text , suffix , nxt = get(url+suffix , nxt)

        # 将文本内容写入一个 .txt 文件
    with open('novel.txt', 'a', encoding='utf-8') as file:
        file.write(content_text)
    time.sleep(0.1)