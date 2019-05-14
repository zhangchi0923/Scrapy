## python爬虫（二）
#### 2.1 Beautiful Soup
Beautiful Soup 是一个可以从HTML和XML文件中提取数据的python库，它可以使用用户喜欢的转换器实现惯用的文档导航，修改，定位等功能。

*由于使用的编译环境是python3，安装bs4时，注意使用pip3命令*

bs有几种解析器，按照不同的需求选择使用：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190512171408280.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RydW5rd2hpc2t5,size_16,color_FFFFFF,t_70)

我们可以把BeautifulSoup类当作对应html或xml文档的全部内容。

###### Tag对象

bs中有几种对象，本次任务主要用到了Tag对象。Tag有两个最重要的属性：name和attribute

- name属性

```
tag.name
tag.name = "blockquot"	# <blockquot>...</blockquot>
```
- attribute属性
  	一个tag可能有很多个属性. `tag <b class="boldest">` 有一个 “class” 的属性,值为 “boldest” . tag的属性的操作方法与字典相同

```
tag[‘class']
# u'boldest'
```
​		也可以用“点”来访问attribute属性（键值对）

```
tag.attr
# {u'class': u'boldest'}
```
​		修改与删除

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
- NavigaleString

  标签内非属性字符串

```python
tag.string	# <>...</>中字符串
```

###### BeautifulSoup遍历HTML文件标签树

- 上行遍历

<table>
  <tr>
    <th>属性</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>.parent</td>
    <td>节点的父亲标签</td>
  </tr>
  <tr>
    <td>.parents</td>
    <td>用于遍历循环先辈节点</td>
  </tr>
</table>

```python
soup = BeautifulSoup(demo,"html.parser")
for parent in soup.parents:
	if parent is None:
		print(parent)
	else:
		print(parent.name)
```

- 平行遍历（必须发生在同一个父亲节点下）

<table>
  <tr>
    <th>属性</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>.next_sibling</td>
    <td>返回按照HTML文本顺序的下一个平行节点标签</td>
  </tr>
  <tr>
    <td>.previous_sibling</td>
    <td>返回按照HTML文本顺序的上一个平行节点标签</td>
  </tr>
  <tr>
    <td>.next_siblings</td>
    <td>迭代类型，返回按照HTML文本顺序的所有后续平行节点标签</td>
  </tr>
  <tr>
    <td>.previous_sibling</td>
    <td>迭代类型，返回按照HTML文本顺序的所有前面平行节点标签</td>
  </tr>
</table>

```python
soup = BeautifulSoup(demo,"html.parser")
# 平行遍历后续节点
for next_sibling in soup.next_siblings:
	print(next_sibling)
	
# 平行遍历前续节点
for previous_sibling in soup.previous_siblings:
	print(previous-sibling)
```

- 下行遍历

<table>
  <tr>
    <th>属性</th>
    <th>说明</th>
  </tr>
  <tr>
    <td>.contents</td>
    <td>子节点列表，将所有儿子节点存入列表</td>
  </tr>
  <tr>
    <td>.children</td>
    <td>子节点迭代类型，用于遍历儿子节点</td>
  </tr>
  <tr>
    <td>.descendants</td>
    <td>子孙节点迭代类型，包含所有子孙节点，用于遍历循环</td>
  </tr>
</table>

```python
# 下行遍历所有儿子节点
for child in soup.children:
	print(child)
	
# 下行遍历所有子孙节点
for descendant in soup.descendants:
	print(descendant)
```

###### 信息标记的三种形式

标记后的信息具有了信息结构，增加了信息维度，从而可用于通信也便于理解。信息的结构与信息具备着同样的价值。

- XML (extensible markup language)

  ```xml
  <img src="demo.jpg" size="10"/>
  <!--This is a comment-->
  ```

- JSON (JavaScript Obeject Notation)

  有数据类型的键值对

  ```json
  "key":"value"
  "key":["value1","value2"]
  "key":{"subkey":"subvalue"}
  ```

- YAML (YAML Ain't Markup Language)

  无数据类型的键值对

  ```yaml
  key:value
  key:#Comment
  -value1			# "-"表示并列的值
  -value2
  key:				# 键值对之间可嵌套
  	subkey:subvalue
  ```

###### 信息提取方法

- 完整解析信息标记形式，再提取关键信息（例如用bs4库的标签遍历树）。信息解析准确，过程繁琐，慢。
- 无视标记形式，直接搜索关键信息，*文本查找函数*即可。简洁、速度快，但准确性与信息本身有关。
- 融合方法，既能解析又能查找。

实例：

提取HTML中所有URL链接

思路：

（1）搜索所有<a>标签

（2）解析<a>标签格式，提取href后的链接内容

```python
<>.find_all(name, attrs, recursive, string, **kwargs)
# <tag>(..)等价于<tag>.find_all(..)
# soup(..)等价于soup.find_all(..)
# find_all()方法的变种：
find_parents()
find_next_siblings
...
```

name：对某个标签名称的检索字符串

attrs：对某个标签属性的检索字符串

recursive：是否对全部子孙检索，默认true

string：<>…</>中字符串区域的检索字符串

使用bs爬取丁香园社区http://www.dxy.cn/bbs/thread/626626#626626 板块下的信息（用户ID，评论时间，评论内容）

```python
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
Xpath筛选出评论信息代码：  

```python
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
爬取结果  
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019051317210951.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RydW5rd2hpc2t5,size_16,color_FFFFFF,t_70)
