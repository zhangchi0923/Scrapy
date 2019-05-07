---
title: Python爬虫学习-Day3
date: 2019-03-03 21:43:34
tags: ['bs4', '爬虫']
categories: ['bs4', '爬虫']
copyright: true
---
###  文章目录

      * 一、Beautiful Soup使用 
        * 1、简介 
        * 2、四大种类对象 
          * 1）Tag 
          * 2）NavigableString 
          * 3）BeautifulSoup 
          * 4）Comment 
        * 3、遍历文档树 
          * 1）直接子节点 
          * 2）所有子孙节点 
          * 3）节点内容 
        * 4、搜索文档树 
          * 1）name参数 
          * 2）text参数 
        * 5、CSS选择器 
          * 1）通过对标签名查找 
          * 2）通过类名查找 
          * 3）通过id名查找 
          * 4）获取内容 
      * 二、丁香园评论爬取 

###  一、Beautiful Soup使用

####  1、简介

昨天用正则表达式来匹配出现诸多问题，一个字符写错都可能导致匹配结果出错，几天学Beautiful Soup库的使用。  
简单来说，Beautiful Soup就是Python的一个HTML或XML的解析库，可以用它来方便的从网页中提取数据。利用它可以省去很多琐碎的提取工作。  
首先利用pip install beautifulsoup4安装库，安装好后在python解析器输入from bs4 import
BeautifulSoup看能否导入成功。注意安装库名与导入的不同，要特别注意。

####  2、四大种类对象

Beautiful Soup将复杂HTML文档转换成一个复杂的树形结构，每个节点都是一个python对象，所有对象可以归纳为四种。

  * Tag 
  * NavigableString 
  * BeautifulSoup 
  * Comment 

#####  1）Tag

Tag通俗点讲就是HTML中的一个个标签，像dl、dt、a、dd、p等HTML标签加上里面包括等内容就是Tag，我们可以用soup加标签名轻松的获取这些标签的内容，这些对象的类型是bs4.element.Tag。  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190303181835367.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    print(soup.title)
    print(soup.head)
    print(soup.p)
    print(soup.a)
    
    结果：
    <title>the dormouse</title>
    <head><title>the dormouse</title>
    </head>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    <a class="sister" href="http://example.com/elsie" id="link1"></a>
    

对于Tag，它有两个重要属性，name和attrs

#####  2）NavigableString

通过上述可以得到标签的内容，而想要获得标签内的文字，可以用.string。

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    print(soup.title)
    print(soup.head)
    print(soup.p)
    print(soup.a)
    
    print(soup.p.string)
    
    结果：
    <title>the dormouse</title>
    <head><title>the dormouse</title>
    </head>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    <a class="sister" href="http://example.com/elsie" id="link1"></a>
    the dormouse's story
    

#####  3）BeautifulSoup

BeautifulSoup对象表示的是一个文档的内容，大部分时候，可以把它当作Tag对象，是一个特殊的Tag，可以分别获取它的类型，名称，以及属性。

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    #print(soup.title)
    #print(soup.head)
    #print(soup.p)
    #print(soup.a)
    #
    #print(soup.p.string)
    
    print(soup.name)
    print(type(soup.name))
    print(soup.attrs)#文档本身的属性为空
    
    结果：
    [document]
    <class 'str'>
    {}
    

#####  4）Comment

Comment对象是一个特殊类型的NavigableString对象，其输出的内容不包括注释符合。

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    print(soup.a)
    print(soup.a.string)
    print(type(soup.a.string))
    
    结果：
    <a class="sister" href="http://example.com/elsie" id="link1"></a>
    None
    <class 'NoneType'>
    

####  3、遍历文档树

#####  1）直接子节点

  * .content属性 

tag的.content属性可以将tag的子节点以列表的方式输出。

  * .children属性 

.children属性返回的不是一个list，而是一个list生成器，不过我们可以通过遍历获取所有的子节点。

#####  2）所有子孙节点

  * .descendants属性 

.contents 和 .children属性仅包含tag的直接子节点，
.descendants属性可以对所有tag的子孙节点进行递归循环，和.children类似，我们也需要遍历获取其中的内容。

#####  3）节点内容

  * .string属性   
如果tag只有一个NavigableString类型子节点，那么这个tag可以使用.string得到子节点，如果tag仅有一个子节点，那么这个tag也可以使用.string方法，输出结果与当前唯一子节点的.string结果相同。即就是如果一个标签里面没有标签了，那么.string就会返回标签里面的内容，如果标签里面只有唯一的一个标签了，那么.string会返回最里面的内容。

####  4、搜索文档树

find_all(name, attrs, recursive, text, **kwargs)

#####  1）name参数

name 参数可以查找所有名字为name的tag，字符串对象会被自动忽略掉  
A、传递字符串  
最简单的过滤器是字符串，在搜索方法中传入一个字符串参数，BeautifulSoup会查找与字符串完整匹配的内容。  
B、传正则表达式  
如果传入正则表达式作为参数，BeautifulSoup会通过正则表达式的match（）来匹配内容，下面例子中找出所有以b开头的标签，这表示和
**标签都应该被找到  
C、传列表  
如果传入列表参数，BeautifulSoup会将与列表中任一元素匹配的内容返回。 **

#####  2）text参数

通过text参数可以搜索文档中的字符串内容，与name参数的可选值一样，text参数接收字符串，正则表达式，列表。

####  5、CSS选择器

  * 写CSS时，标签名不加任何修饰，类名前加.，id名前加# 
  * 用方法soup.select（），返回类型时list 

#####  1）通过对标签名查找

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    print(soup.select('title'))
    print(soup.select('a'))
    print(soup.select('p'))
    
    结果：
    [<title>the dormouse</title>]
    [<a class="sister" href="http://example.com/elsie" id="link1"></a>]
    [<p class="title" name="dromous"><b>the dormouse's story</b></p>]
    

#####  2）通过类名查找

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    print(soup.select('.sister'))
    
    结果：
    [<a class="sister" href="http://example.com/elsie" id="link1"></a>]
    

#####  3）通过id名查找

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html)
    
    print(soup.select('#link1'))
    
    结果：
    [<a class="sister" href="http://example.com/elsie" id="link1"></a>]
    

#####  4）获取内容

以上的select方法返回的结果都是列表形式，可以遍历输出，然后用get_text()方法来获取它的内容。

    
    
    from bs4 import BeautifulSoup
    
    html = """
    <head><title>the dormouse</title></hed>
    <a class="sister" href="http://example.com/elsie" id="link1"<!--elsie--></a>
    <p class="title" name="dromous"><b>the dormouse's story</b></p>
    """
    
    soup = BeautifulSoup(html, 'lxml')
    print(type(soup.select('title')))
    print(soup.select('title')[0].get_text())
    
    for title in soup.select('title'):
        print(title.get_text())
    
    结果：
    
    <class 'list'>
    the dormouse
    the dormouse
    

###  二、丁香园评论爬取

    
    
    from bs4 import BeautifulSoup
    import requests
    
    
    def get_one_page(url):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 14_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    
    
    if __name__ == "__main__":
        url = 'http://www.dxy.cn/bbs/topic/509959?keywords=%E6%99%95%E5%8E%A5%E5%BE%85%E6%9F%A5%E2%80%94%E2%80%94%E8%AF%B7%E6%95%99%E5%90%84%E4%BD%8D%E5%90%8C%E4%BB%81+-+%E5%BF%83%E8%A1%80%E7%AE%A1%E4%B8%93%E4%B8%9A%E8%AE%A8%E8%AE%BA%E7%89%88+-%E4%B8%81%E9%A6%99%E5%9B%AD%E8%AE%BA%E5%9D%9B%E2%80%8B+'
        html = get_one_page(url)
        items = BeautifulSoup(html, 'lxml')
        
    
        use_id = items.select('div[class="auth"]')#[0].get_text()
        content = items.select('td[class="postbody"]')#[0].get_text()
        L = []
        for uses,ss in zip(use_id,content):
            a = "用户：" + uses.get_text().strip()
            b = "回复内容：" + ss.get_text().strip()
            dic = {a:b}
            L.append(dic)
        print(L)
    #    print(use_id)
    #    print(content)
    
    结果：
    [{'用户：楼医生': '回复内容：我遇到一个“怪”病人，向大家请教。她，42岁。反复惊吓后晕厥30余年。每次受响声惊吓后发生跌倒，短暂意识丧失。无逆行性遗忘，无抽搐，无口吐白沫，无大小便失禁。多次跌倒致外伤。婴儿时有惊厥史。入院查体无殊。ECG、24小时动态心电图无殊；头颅MRI示小软化灶；脑电图无殊。入院后有数次类似发作。请问该患者该做何诊断，还需做什么检查，治疗方案怎样？'}, {'用户：lion000': '回复内容：从发作的症状上比较符合血管迷走神经性晕厥，直立倾斜试验能协助诊断。在行直立倾斜实验前应该做常规的体格检查、ECG、UCG、holter和X-ray胸片除外器质性心脏病。贴一篇“口服氨酰心安和依那普利治疗血管迷走性晕厥的疗效观察”作者：林文华 任自文 丁燕生http://www.ccheart.com.cn/ccheart_site/Templates/jieru/200011/1-1.htm'}, {'用户：xghrh': '回复内容：同意lion000版主的观点：如果此患者随着年龄的增长，其发作频率逐渐减少且更加支持，不知此患者有无这一特点。入院后的HOLTER及血压监测对此患者只能是一种安慰性的检查，因在这些检查过程中患者发病的机会不是太大，当然不排除正好发作的情况。对此患者应常规作直立倾斜试验，如果没有诱发出，再考虑有无可能是其他原因所致的意识障碍，如室性心动过速等，但这需要电生理尤其是心腔内电生理的检查，毕竟是有一种创伤性方法。因在外地，下面一篇文章可能对您有助，请您自己查找一下。心理应激事件诱发血管迷走性晕厥1例 ，杨峻青、吴沃栋、张瑞云，中国神经精神疾病杂志， 2002 Vol.28 No.2'}, {'用户：keys': '回复内容：该例不排除精神因素导致的，因为每次均在受惊吓后出现。当然，在作出此诊断前，应完善相关检查，如头颅MIR(MRA),直立倾斜试验等。'}]
    

