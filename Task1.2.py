# -*- coding: UTF-8 -*-
import requests
import re
import json
for i in range(0,250,25):

    url = 'https://movie.douban.com/top250?start={}&filter='.format(i)  # 翻页循环设置：通过对start赋值以25的倍数
    html = requests.get(url).text
    regex = '<em class="">(\d+)</em>.*?<span class="title">(.*?)</span>.*?<p class="">(.*?)</p>.*?<span class="rating_num" property="v:average">(.*?)</span>.*?<span>(.*?)</span>.*?<span class="inq">(.*?)</span>'
    pattern = re.compile(regex, re.S)
    results = re.findall(pattern, html)



    #处理得到的结果
    for item in results:
        content = ""
        for every_list in item[2].split():
            content = content + "".join(every_list)
        content = re.sub('&nbsp;', ' ', content)
        content = re.sub('<br>', '', content)
        print(content)

        #将得到的信息存储在字典中
        dict = {
            "排名": item[0],
            "影片": item[1],
            "描述": item[2],
            "主演": item[3],
            "评分": item[4],
            "标签": item[5]

        }
        with open('豆瓣电影top250.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(dict, ensure_ascii=False) + '\n')
