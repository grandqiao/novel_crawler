#适配于 笔趣阁(http://www.ibiqu.net/) 该类网站


import re

import requests
from bs4 import BeautifulSoup
import time


def delete_text(content_text , unwanted_text):
    cleaned_text = content_text.replace(unwanted_text, "")
    return cleaned_text

def get(url , next_bool):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    head_div = soup.find('h1')
    head_text = head_div.get_text() if head_div else ''

    content_div = soup.find('div', id='content', class_='c2' )



    paragraphs = content_div.find_all('p')
    content_text = '\n'.join(p.get_text() for p in paragraphs)

    # print(content_text)


    unwanted_text = ["小主，这个章节后面还有哦^.^，请点击下一页继续阅读，后面更精彩！" , "这章没有结束^.^，请点击下一页继续阅读！" , "喜欢修真四万年请大家收藏：(m.shaonianshuwu.com)修真四万年少年书屋更新速度全网最快。","本小章还未完~.~，请点击下一页继续阅读后面精彩内容！"]
    for i in unwanted_text:
        content_text = delete_text(content_text, i)

    if next_bool == 1:
        content_text = "\n\n\n"+head_text+"\n"+content_text
    # 查找包含“下一页”文本的 <a> 标签
    next_page_tag = soup.find('a', text="下一页")

    nxt = 0

    # print(soup)

    # 提取并打印该标签的 href 属性
    if next_page_tag:
        next_page_href = next_page_tag['href']
    else:
        print(head_text+" 已结束")
        next_page_tag = soup.find('a', text="下一章")
        next_page_href = next_page_tag['href']
        nxt = 1


    print("Next page href:", next_page_href)
    return content_text , next_page_href , nxt


url = "http://www.ibiqu.net"
suffix = "/147_147321/177839575.html"   #需要添加的书籍，第一章url
nxt = 1

for i in range(5):
    content_text , suffix , nxt = get(url+suffix , nxt)

        # 将文本内容写入一个 .txt 文件
    with open('content.txt', 'a', encoding='utf-8') as file:
        file.write(content_text)
    time.sleep(0.1)