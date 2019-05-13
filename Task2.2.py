import requests
from lxml import etree

def getHTML(url,hd):
    try:
        r = requests.request("GET",url,headers = hd)
        r.raise_for_status()
        r.encoding = 'utf-8'
        html = r.text
        return html
    except:
        return "Exception!"

def getInfo(html):
    content = etree.HTML(html)
    etree.strip_tags(content, "<br />")
#   user_id = content.xpath('//div[@class="auth"]//text()')
#   post_time = content.xpath('//div[@class="post-info"]/span[1]//text()')
    comment = content.xpath('//td[@class="postbody"]//text()')

    for i in range(len(comment)):
        # print("用户: "+user_id[i].strip())
        # print("时间: "+post_time[i].strip())
        print(comment[i].strip())


if __name__ == "__main__":
    url = "http://www.dxy.cn/bbs/thread/626626"
    hd = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    html = getHTML(url,hd)
    getInfo(html)