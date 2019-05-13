## python爬虫（二）
#### 2.1 Beautiful Soup
Beautiful Soup 是一个可以从HTML和XML文件中提取数据的python库，它可以使用用户喜欢的转换器实现惯用的文档导航，修改，定位等功能。

*由于使用的编译环境是python3，安装bs4时，注意使用pip3命令*

bs有几种解析器，按照不同的需求选择使用：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190512171408280.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RydW5rd2hpc2t5,size_16,color_FFFFFF,t_70)
###### Tag对象
bs中有几种对象，本次任务主要用到了Tag对象。Tag有两个最重要的属性：name和attribute
*name属性*
```
tag.name
tag.name = "blockquot"
```
*attribute属性*
一个tag可能有很多个属性. `tag <b class="boldest">` 有一个 “class” 的属性,值为 “boldest” . tag的属性的操作方法与字典相同
```
tag[‘class']
# u'boldest'
```
也可以用“点”来访问attribute属性

```
tag.attr
# {u'class': u'boldest'}
```
修改与删除

```
tag['class'] = 'verybold'
tag['id'] = 1
tag
# <blockquote class="verybold" id="1">Extremely bold</blockquote>

del tag['class']
del tag['id']
tag
# <blockquote>Extremely bold</blockquote>

tag['class']
# KeyError: 'class'
print(tag.get('class'))
# None
```
使用bs爬取丁香园社区http://www.dxy.cn/bbs/thread/626626#626626某一板块下的信息（用户ID，评论时间，评论内容）

```
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

#打印网页源码
print(requests.get(url,headers = hd).text)

#使用bs获取网页文件，并使用lxml解析器
soup = bs(response,features="lxml")
#打印'a'节点中的链接
for link in soup.find_all('a'):
    print(link.get('href'))

#打印'p'节点的内容
print(soup.p)

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
```
爬取结果
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190512202829301.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RydW5rd2hpc2t5,size_16,color_FFFFFF,t_70)
#### 2.2 XPath
Xpath是一门在在XML文件中查找信息的语言，我们也可以用来对html文件进行查找。

##### Xpath基本语法
<table>
<h4>路径表达式：</h4>
  <tr>
    <th>表达式</th>
    <th>描述</th>
  </tr>
  <tr>
    <td>nodename</td>
    <th>选区此节点的所有子节点</th>
  </tr>
  <tr>
    <td>/</td>
    <td>从根节点选取</td>
  </tr>
  <tr>
    <td>//</td>
    <td>从当前节点中选取文档中所有节点，无论位置</td>
  </tr>
  <tr>
    <td>.</td>
    <td>选取当前节点</td>
  </tr>
  <tr>
    <td>..</td>
    <td>选取当前节点的父节点</td>
  </tr>
  <tr>
    <td>@</td>
    <td>选取属性</td>
  </tr>
</table>

<table>
<h4>常见带有谓语的路径表达式及其结果：</h4>
  <tr>
    <th>路径表达式</th>
    <th>结果</th>
  </tr>
  <tr>
    <td>/bookstore/book[1]</td>
    <td>选取属于bookstore元素的第一个book元素</td>
  </tr>
  <tr>
    <td>/bookstore/book[last()]</td>
    <td>选取属于bookstore元素的最后一个book元素</td>
  </tr>
  <tr>
    <td>/bookstore/book[last()-1]</td>
    <td>选取属于bookstore元素的倒数第二个book元素</td>
  </tr>
  <tr>
    <td>/bookstore/book[position()<3]</td>
    <td>选取属于bookstore元素的前两个book元素</td>
  </tr>
  <tr>
    <td>//title[@lang]</td>
    <td>选取所有拥有lang属性的title元素</td>
  </tr>
  <tr>
    <td>//title[@lang='eng']</td>
    <td>选取所有lang属性的值为eng的title元素</td>
  </tr>
  <tr>
    <td>/bookstore/book[price>35.00]</td>
    <td>选取属于bookstore元素的所有book元素，且其price元素大于35.00</td>
  </tr>
  <tr>
    <td>/bookstore/book[price>35.00]/title</td>
    <td>选取属于bookstore元素的所有price元素大于35.00的book元素中的title元素</td>
  </tr>
</table>
利用Xpath筛选评论信息代码
```
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
```
屏幕快照 2019-05-13 下午5.19.55
