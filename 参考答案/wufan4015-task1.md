---
title: Python爬虫学习-Day1
date: 2019-03-01 21:31:07
tags: []
categories: []
copyright: true
---
###  一、爬虫简介及网页知识

    
    
       今天开始学习爬虫，用一周的时间强化学习，坚持下来就是胜利。
       随着技术的不断发展，大数据的时代已经到来，数据的获取途径有两条，买数据或者利用工具爬取数据。
       根据使用场景，爬虫分为通用爬虫和聚焦爬虫两种。通用爬虫是搜索引擎抓取系统的重要组成部分，例如谷歌、百度、雅虎等，主要目的是将互联网上的网页下载到本地，形成一个互联网内容的镜像备份。聚焦爬虫，是面向特定主题需求的一种网络爬虫，与通用爬虫的区别是在抓取数据内容时进行数据处理筛选，尽量保证只抓取与需求相关的网页信息。
       提取信息后，我们一般会将提取到的数据保存到某处以便后续继续使用。这里保存形式多种多样，可以简单保存为TXT文本或JSON文本，也可以保存到数据库，如MySQL和MongoDB等，也可以保存到远程服务器，如借助SFTP进行操作。
    

#####  1、HTTP和HTTPS

**HTTP协议（超文本传输协议）：** 是一种发布和接收HTML页面的方法。  
**HTTPS：** 简单讲就是HTTP的安全版，在HTTP下加入SSL层。  
**浏览器发送HTTP请求的过程：**  
1）当用户在浏览器的地址栏输入一个URL后，浏览器会向HTTP服务器发送HTTP请求，主要分为Get和 Post两种方法。  
2）当我们在浏览器输入URL [ http://www.baidu.com ](http://www.baidu.com)
的时候，浏览器发送一个Request请求去获取网站的HTML文件，服务器把Response文件对象发送给浏览器。  
3）浏览器分析Response中的HTML，发现其中引用了很多其他文件，浏览器会自动再次发送Request去获取其他文件。  
4）当所有的文件都下载成功后，网页会根据HTML语法结构，完整的显示出来。  
**URL：** 统一资源定位符，用于描述网页和其他资源地址的一种标示方法。  
基本格式：scheme://host[:port#]/path/…/[?query-string][#anchor]

  1. scheme: 协议（例如：http, https, ftp） 
  2. host: 服务器的ip地址或者域名 
  3. port#: 服务器端口（如果是走默认协议端口，缺省80） 
  4. path: 访问资源的路径 
  5. query-string: 参数，发送给http服务器的数据 
  6. anchor: 锚（跳转到网页的指定锚点为止）   
HTTP1.1：完善的请求/响应模型，并将协议补充完整，请求方法如下。

序号  |  方法  |  描述  
---|---|---  
1  |  GET  |  请求指定的页面信息，并返回实体主体  
2  |  HEAD  |  类似于get请求，只不过返回的响应体中没有具体的内容，用于获取报头  
3  |  POST  |  向指定资源提交数据进行处理请求，数据被包含在请求体中，POST请求会导致新的资源建立或已有资源的修改  
4  |  PUT  |  从客户端向服务器传送的数据取代指定的文档的内容  
5  |  DELETE  |  请求服务器删除指定页面  
6  |  CONNECT  |  HTTP/1.1协议中预留给能够将链接改为通道方式的代理服务器  
7  |  OPTIONS  |  允许客户端查看服务器的性能  
8  |  TRACE  |  回显服务器收到的请求，主要用于测试或诊断  
  
GET是向服务器上获取数据，POST是向服务器传送数据。  
注意，避免使用get方式请求提交表单，因为可能回导致安全问题。

#####  2、常用的请求报头

1）Host（主机和端口号）  
对应网址URL中的web名称和端口号，通常属于URL的一部分  
2）Connection（链接类型）  
Client发起一个包含Connection：keep-alive的请求，HTTP1.1使用默认值。  
server收到请求后，回复一个包含Connection：keep-alive的响应，不关闭链接（支持keep-
alive）或者Connection：close的响应，关闭链接（不支持keep-alive）。  
3）Upgrade-Insecure-Requests（升级为HTTPS请求）  
HTTPS是以安全为目的的HTTP通道，所以在HTTPS承载页面上不允许HTTP请求，一旦出现就提示或报错。  
4）User-Agent（浏览器名称）  
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36
(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36  
5）Accept（传输文件类型）  
指浏览器或其他客户端可以接受的MIME文件类型，服务器可以根据它判断并返回适当的文件格式。  
6）Referer（页面跳转处）  
表明产生请求的网页来自于哪个URL，用户是从该Referer页面访问到当前请求的页面，这个属性可以用来跟踪web请求来自哪个页面，是从什么网站来的等。  
7）Accept-Encoding（文件编码格式）  
指出浏览器可以接受的编码方式，编码方式不同于文件格式，它是为了压缩文件并加速文件传递速度，在接收到web响应后先解码，然后再检查文件格式，可以减少大量的下载时间。  
8）Accept-Language（语言种类）  
Accept-Language: zh-CN,zh;q=0.9  
9）Content-Type（POST数据类型）  
请求里用来表示的数据类型  
Content-Type: text/html; charset=UTF-8  
10）Cookie  
是在浏览器中寄存的小型数据体，可以记载和服务器相关的用户信息。

#####  3、常见状态码：

  * 100～199：表示服务器成功接收部分请求，要求客户端继续提交其余请求才能完成整个处理过程。 
  * 200～299：表示服务器成功接收请求并完成整个处理过程，常用200OK 
  * 300～399：为完成请求，客户需进一步细化请求。常用302请求页面已临时转移至新URL，304/307使用缓存资源。 
  * 400～499：客户端的请求有错误，常用404服务器无法找到被请求的页面，403服务器拒绝访问权限不够。 
  * 500～599：服务器端出现错误，常用500请求未完成，服务器遇到不可预知的情况。 

###  二、urllib库的使用

    
    
       在Python2中，有urllib和urllib2两个库来实现请求到发送。而在Python3中，已经不存在urllib2这个库来，统一为rullib，其官方文档链接为：https://docs.python.org/3/library/urllib.html。
    

  * request：它是最基本的HTTP请求模块，可以用来模拟发送请求。就像浏览器输入网址然后回车一样，只需要给库方法传入URL以及额外的参数，就可以模拟实现这个过程了。 
  * error：异常处理模块，如果出现请求错误，我们可以捕获这些异常，然后进行重试或其他操作以保证程序不会意外终止。 
  * parse：一个工具模块，提供了许多URL处理方法，比如拆分、解析、合并等。 
  * robotparse：主要用来识别网站等robots.txt文件，然后判断哪些网站可以爬，哪些网站不可以爬，它其实用的比较少。 

####  1、urlopen

    
    
    import urllib.request
    
    url = 'http://www.baidu.com'
    response = urllib.request.urlopen(url=url)#利用urlopen可以完成简单的网页的GET请求抓取
    #print(response.read().decode('utf-8'))
    print(type(response))#返回response的类型
    print(response.getheaders())#返回头部信息
    print(response.getheader('Server'))#返回Server的信息
    print(response.status)#返回状态码
    
    
    运行结果：
    <class 'http.client.HTTPResponse'>
    #它是一个HTTPResponse类型的对象，主要包含read()、readinto（）、getheader（name）、getheaders（）、fileno（）等方法。
    
    [('Bdpagetype', '1'), ('Bdqid', '0xabc37c350007fc04'), ('Cache-Control', 'private'), ('Content-Type', 'text/html'), ('Cxy_all', 'baidu+929ba400c65d0f0d884326bfb781dda4'), ('Date', 'Fri, 01 Mar 2019 12:55:16 GMT'), ('Expires', 'Fri, 01 Mar 2019 12:55:01 GMT'), ('P3p', 'CP=" OTI DSP COR IVA OUR IND COM "'), ('Server', 'BWS/1.1'), ('Set-Cookie', 'BAIDUID=8350FC53AE71FE4915D12FAF458401D4:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com'), ('Set-Cookie', 'BIDUPSID=8350FC53AE71FE4915D12FAF458401D4; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com'), ('Set-Cookie', 'PSTM=1551444916; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com'), ('Set-Cookie', 'delPer=0; path=/; domain=.baidu.com'), ('Set-Cookie', 'BDSVRTM=0; path=/'), ('Set-Cookie', 'BD_HOME=0; path=/'), ('Set-Cookie', 'H_PS_PSSID=1445_21107_18560_28585_26350_28603; path=/; domain=.baidu.com'), ('Vary', 'Accept-Encoding'), ('X-Ua-Compatible', 'IE=Edge,chrome=1'), ('Connection', 'close'), ('Transfer-Encoding', 'chunked')]
    
    BWS/1.1
    
    200
    

#####  2、request

    
    
    	如果请求中需要加入Headers等信息，就可以利用更强大的Request类来构建。
    	Request的参数构造
    	class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, mathod=None)
    

  * 第一个参数url用于请求URL，这是必传参数，其他参数都是可选的。 
  * 第二个参数data如果要传，必须传bytes（字节流）类型的，如果它是字典，可以先用urllib.parse模块里的urlencode（）编码。 
  * 第三个参数headers是一个字典，它就是请求头，我们可以在构造请求时通过headers参数直接构造，也可以通过调用请求实例的add_header()方法添加（）如下：   
` 'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us)
AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50' `

  * 第四个参数origin_req_host 指的是请求方的host名称或者IP地址。 
  * 第五个参数unverifiable表示这个请求是否是无法验证的，默认是False，意思就是说用户没有足够权限来选择接收这个请求的结果。 
  * 第六个参数method是一个字符串，用来指示请求使用的方法，比如GET、POST、和PUT等。 

    
    
    from urllib import request, parse
    url = 'http://httpbin.org/post'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Host':'httpbin.org'
               }
    dict = {'name':'Germey'}
    data = bytes(parse.urlencode(dict), encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))
    
    
    输出结果：
    {
      "args": {}, 
      "data": "", 
      "files": {}, 
      "form": {
        "name": "Germey"
      }, 
      "headers": {
        "Accept-Encoding": "identity", 
        "Cache-Control": "max-age=259200", 
        "Content-Length": "11", 
        "Content-Type": "application/x-www-form-urlencoded", 
        "Host": "httpbin.org", 
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
      }, 
      "json": null, 
      "origin": "221.178.182.60, 221.178.182.60", 
      "url": "https://httpbin.org/post"
    }
    

###  三、requests库的使用

#####  1、GET请求

HTTP中最常见的请求，首先构建一个简单的GET请求。

    
    
    import requests
    
    r = requests.get('http://httpbin.org/get')
    print(type(r.text))
    print(r.json())
    print(type(r.json()))
    
    结果:
    <class 'str'>
    {'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Cache-Control': 'max-age=259200', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.21.0'}, 'origin': '221.178.182.141, 221.178.182.141', 'url': 'https://httpbin.org/get'}
    <class 'dict'>
    

可以发现，调用json（）方法，就可以将返回结果是JSON格式的字符串转化为字典。  
如果返回结果不是JSON格式，便会返回解析错误。

#####  2、POST请求

直接上代码：

    
    
    import requests
    
    data = {'name': 'germey', 'age': '22'}
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Host':'httpbin.org'
               }
    r = requests.post('http://httpbin.org/post', headers=headers, data=data)
    print(r.text)
    
    运行结果:
    {
      "args": {}, 
      "data": "", 
      "files": {}, 
      "form": {
        "age": "22", 
        "name": "germey"
      }, 
      "headers": {
        "Accept": "*/*", 
        "Accept-Encoding": "gzip, deflate", 
        "Cache-Control": "max-age=259200", 
        "Content-Length": "18", 
        "Content-Type": "application/x-www-form-urlencoded", 
        "Host": "httpbin.org", 
        "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
      }, 
      "json": null, 
      "origin": "221.178.182.49, 221.178.182.49", 
      "url": "https://httpbin.org/post"
    }
    

可以发现，我们成功获得了返回结果，其中form部分就是提交的数据，这就证明POST请求成功发送了。

