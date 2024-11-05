#适配于 少年书屋(https://m.shaonianshuwu.com/)


import re

import requests
from bs4 import BeautifulSoup
import time


def delete_text(content_text , unwanted_text):
    cleaned_text = content_text.replace(unwanted_text, "")
    return cleaned_text

def cal_char(url):
    import re

    # 给定的字符串
    url = "com/12239/648296/1.html"

    # 使用正则表达式匹配以 'com' 开头的部分，并计算其后的斜杠数量
    match = re.match(r'^com(.*?)$', url)
    if match:
        slashes_after_com = match.group(1).count('/')
    else:
        slashes_after_com = 0
    return slashes_after_com
def get(url , next_bool):
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)
    head_div = soup.find('h1', class_='headline')
    content_div = soup.find('div', class_='content')

    content_text = content_div.get_text()  # 提取文本内容，不包括 HTML 标签
    head_text = head_div.get_text()

    unwanted_text = ["小主，这个章节后面还有哦^.^，请点击下一页继续阅读，后面更精彩！" , "这章没有结束^.^，请点击下一页继续阅读！" , "喜欢修真四万年请大家收藏：(m.shaonianshuwu.com)修真四万年少年书屋更新速度全网最快。","本小章还未完~.~，请点击下一页继续阅读后面精彩内容！"]
    for i in unwanted_text:
        content_text = delete_text(content_text, i)

    if next_bool == 1:
        content_text = head_text+"\n"+content_text
    # 查找包含“下一页”文本的 <a> 标签
    next_page_tag = soup.find('a', text="下一页")

    nxt = 0

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


url = "https://m.shaonianshuwu.com"
suffix = "/12239/648296.html"   #需要添加的书籍，第一章url
nxt = 1

for i in range(1000):
    content_text , suffix , nxt = get(url+suffix , nxt)

        # 将文本内容写入一个 .txt 文件
    with open('content.txt', 'a', encoding='utf-8') as file:
        file.write(content_text)
    time.sleep(0.1)