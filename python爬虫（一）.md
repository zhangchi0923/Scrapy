## python网络爬虫（一）
#### 1.get与post请求
##### 关于HTTP
超文本传输协议（HTTP）目的是保证客户端与服务器端的通信，其作用就是实现客户端与服务器的请求-应答。
##### Get与Post
Get和Post是HTTP最常用的两种方法（除此之外还有HEAD,PUT,DELETE等）
- Get：从指定的资源请求数据
- Post：向指定的资源提交要处理的数据

两种请求都可以用requests包中的get方法，post请求可以添加
```
import requests


#get请求

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
try:
    #requests.get()构造了一个Request对象向服务器发送请求，该函数返回一个Response对象，包含从服务器获取的全部内容
    response = requests.get("http://www.baidu.com/",headers = headers)
except requests.HTTPError as e:
    # print(response.text)
     print(response.status_code)	#打印状态码

#post请求，向http://www.douban.com/login发送登录信息
formdata = {'form_email':'1099327299@qq.com','form_password':'password'}
response = requests.post('http://www.douban.com/login',formdata)

```
get与post请求的区别
|  | get | post |
|--|--|--|
| 书签 | 可收藏为书签 | 不可收藏为书签 |
| 缓存 | 能被缓存 | 不能被缓存 |
| 历史 | 参数会保留在浏览器历史记录中 | 参数不会保留在浏览器历史记录中 |
|数据长度限制  | 有限制。URL最大长度为2048个字符 | 无限制，且允许二进制 |
| 安全性 | 相比于post较差，因为发送的数据是url的一部分 | 比较安全 |
| 可见行 | 数据在url中对所有人可见 | 数据不显示在url中 |

不同状态码代表含义
```

	状态码				原因短语     				含义

	100				Continue 		说明收到了请求的初始部分，请客户端继续，发送了这个状态码之后，
											服务器在收到请求之后必须进行响应。

	101				Switching Protocols 说明服务器正在根据客户端的指定，将协议切换成Update首部所列的
											协议

	200 				OK					请求没问题，实体的主体部分包含了所请求的资源

	201 				Created				用于创建服务器对象的请求（比如，PUT）。响应的实体主体部分中
								应该包含各种引用了已创建的资源的URL，Location首部包含的则是最具体的引用。

	202 				Accepted		请求已被接受，但服务器还未对其执行任何动作。不能保证服务器会完成这
								个请求；这只是意味着接受请求时，它看起来是有效的。服务器应该在实体的主体部
								分包含对请求状态的描述，或许还应该有对请求完成时间的估计（或者包含一个指
								针，指向可以获取此信息的位置）

    203 				Non-Authoritative           实体首部包含的信息不是来自原远端服务器，而是来自于资源的一份副本。 
    					Information 		如果中间节点上有一份资源副本，但无法或者没有对它所发送的与资源有关的
    										元信息进行验证，就会出现这种情况

    204					No 	Content         响应报文中包含若干首部和一个状态行，但没有实体的主体部分。主要用于在
    								浏览器不转为显示新文档的情况下，对其进行更新（比如刷新一个表单页面）

    205					Reset Content 		另一个主要用于浏览器的代码。负责告知浏览器清除当前页面中的所有HTML
    										表单元素

    206					Partial Content 	成功执行了一个部分或Range(范围)请求。稍后我们会看到，客户端可以通过
    							一些特殊的首部来获取部分或某个范围内的文档————这个状态码就说明范围请求成功了。


    注：在对那些包含了重定向状态码的非HEAD请求进行响应时，最好要包含一个实体，并在实体中包含描述信息和指向（多个）重定向URL的链接。如：

    HTTP/1.1 301 OK
    Location: http://www.gentle-grooming.com/
    Content-Length: 56
    Content-Type: text/plain

    Please go to our partner site,
    www.gentle-grooming.com



    300					Multiple Choices 	客户端请求一个实际指向多个资源的URL时会返回这个状态码，比如服务器
    										上有某个HTML文档的英语和法语版本。返回这个代码时会带有一个选项列表；这样用户就可以选择它希望使用的那一项了。有多个版本可用时，客户端需要沟通解决。

    301					Moved Permanently	在请求的URL已被移除时使用。响应的Location首部中应该包含资源现在所处
    										的URL

    302 				Found 			与301状态码类似，但是，客户端应该使用Location首部给出的URL来临时定位
    										资源。将来的请求仍应该使用老的URL

    303 				See Other 		告知客户端应该用另一个URL来获取资源。新的URL位于响应报文的Location
    								首部。其主要母的是允许POST请求的响应将客户端定向到某个资源上去

    304  				Not Modified 		客户端可以通过所包含的请求首部，使其请求变成有条件的。如果客户端发起
    								了一个条件GET请求，而最近资源未被修改的话，就可以用这个状态码来说明
    								资源未被修改。带有这个状态码的响应不应该包含实体的主体部分。

    305 				Use Proxy  		用来说明必须通过一个代理访问资源；代理的位置由Location首部给出。很
    								重要的一点是，客户端是相对某个特定资源来解析这条响应的，不能假定所有请求。
								甚至所有对持有请求资源的服务器的请求都通过这个代理进行。如果客户端错误地让
								代理介入了某条请求，可能会引发破坏性的行为，而且会造成安全漏洞。

   	307				Temporary Redireat 	与301状态码类似；但客户端应该使用Location首部给出的URL来临时定位资源
   								。将来的请求应该使用老的URL


   	400 				Bad Request 		用于告知客户端发起了一个错误的请求

   	401 				Unauthorized 		返回适当的首部，用于获取客户端访问资源的权限

   	402         			Payment Required    	此状态码未使用，保留

   	403                	 F	orbidden           	服务器拒绝请求，可在响应主体中告知原因

   	404  				Not Found           	用于告知客户端请求的资源在服务器不存在

   	405 				Method Not Allowd   	告知客户端不支持当前方法，并在Allow首部返回支持的方法

   	406 				Not Acceptable     	没有客户端支持的资源类型

   	407 				Proxy Authentication  	跟401类似，不过用户代理服务器
   						Requireed 

   	408 				Request Timeout     	超时提醒

   	409      			Conflict            	请求会造成服务器冲突

   	410  	            Gone   				跟404一样，只不过服务器曾经拥有过该请求资源

   	411 				Length Required    	要求客户端发送Content-Length首部

   	412 				Precondition Failed  	部分条件验证不通过

   	413   				Request Entity Too Large 客户端发送的主体超过了服务器的希望的长度

   	414 				Request  URL Too Long   客户端请求的时间比服务希望的时间长

   	415 				Unsupported Media Type 	服务器无法理解客户端请求的主体类型

   	416 				Requested Range Not    	请求报文所请求的是指定资源的某个范围，而此范围无效或无法满足时
   						Satisfiable  	，使用此状态码

   	417				Expectation Failed 		请求中包含Expect首部，服务器无法满足

   	500				Internal Server Error  	服务器错误

   	501 				Not Implemented         请求超出了服务器能处理的范围

   	502 				Bad Gateway 		作为代理或网关使用的服务器从请求响应链的下一条链路上收到了一条
   								伪响应（比如，它无法连接到其父网关）时，使用此状态码

   	503    				Service Unavailable 	用来说明服务器现在无法为请求提供服务，但将来可以。如果服务器
   								知道什么时候资源会变为可用的，可以在响应中包含包含一个Retry-After首部。

   	504 				Gateway Timeout 	与状态码408类似，只是这里的响应来自一个网关或代理，它们在等待另
   												一服务器对其请求进行响应时超时了

    505 				HTTP Version Not        服务器收到的请求使用了它无法或不愿支持的协议版本时，使用此
    					Supported 				状态码。有些服务器应用程序会选择不支持协议的早起版本	


```

#### 2.正则表达式
正则表达式是用特定的表达式来匹配检索出的内容从而得到我们想要的信息

下面是用正则表达式爬取豆瓣电影排行top250相关信息

```
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

```
效果图
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019051123303346.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RydW5rd2hpc2t5,size_16,color_FFFFFF,t_70)
