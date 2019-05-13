# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup as bs
import urllib.request
import requests

#url和headers
url = 'http://www.dxy.cn/bbs/thread/626626'
hd = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

req = urllib.request.Request(url,headers=hd)
response = urllib.request.urlopen(req).read().decode("utf-8")

# #打印网页源码
# print(requests.get(url,headers = hd).text)
#
# #使用bs获取网页文件，并使用lxml解析器
soup = bs(response,"lxml")

#从爬取的源码我们可以发现我们要的ID，时间，评论内容等保存在相应的节点中（<div class="auth">等）
for data in soup.find_all("tbody"):
    try:
        user_id = data.find("div", class_="auth").get_text(strip=True)
        print("user_id: "+user_id)
        time = data.find("div", class_="post-info").get_text(strip=True)
        print("post_time: "+time)
        comment = data.find("td",class_="postbody").get_text(strip=True)
        print("comment: "+comment)
    except:
        pass

