---
title: 爬虫学习Day6：ip
date: 2019-03-06 08:36:59
tags: []
categories: ['爬虫学习']
copyright: true
---
###  文章目录

  * 任务 
  * 为什么会出现IP被封 
  * 如何应对IP被封的问题 
  * 获取代理IP地址 
  * 使用代理 
  * 确认代理IP地址有效性 
  * 关于http和https代理 
  * 使用的有用户名和密码认证的代理 

#  任务

【Task6 学习IP相关知识】：（1天）

学习什么是IP，为什么会出现IP被封，如何应对IP被封的问题。

抓取西刺代理，并构建自己的代理池。

西刺直通点： [ https://www.xicidaili.com/ ](https://www.xicidaili.com/)

#  为什么会出现IP被封

网站为了防止被爬取，会有反爬机制，对于同一个IP地址的大量同类型的访问，会封锁IP，过一段时间后，才能继续访问

#  如何应对IP被封的问题

有几种套路：

  1. 修改请求头，模拟浏览器（而不是代码去直接访问）去访问 
  2. 采用代理IP并轮换 
  3. 设置访问时间间隔 

#  获取代理IP地址

从该网站获取： [ https://www.xicidaili.com/ ](https://www.xicidaili.com/)  
inspect -> 鼠标定位：  
要获取的代理IP地址，属于class = "odd"标签的内容：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306182248769.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)  
代码如下，获取的代理IP保存在proxy_ip_list列表中

    
    
    from bs4 import BeautifulSoup
    import requests
    import time
    
    def open_proxy_url(url):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        headers = {'User-Agent': user_agent}
        try:
            r = requests.get(url, headers = headers, timeout = 20)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('无法访问网页' + url)
    
    
    def get_proxy_ip(response):
        proxy_ip_list = []
        soup = BeautifulSoup(response, 'html.parser')
        proxy_ips  = soup.select('.odd')
        for proxy_ip in proxy_ips:
            ip = proxy_ip.select('td')[1].text
            port = proxy_ip.select('td')[2].text
            protocol = proxy_ip.select('td')[5].text
            if protocol in ('HTTP','HTTPS'):
                proxy_ip_list.append(f'{protocol}://{ip}:{port}')
        return proxy_ip_list
    
    if __name__ == '__main__':
        proxy_url = 'https://www.xicidaili.com/'
        text = open_proxy_url(proxy_url)
        proxy_ip_filename = 'proxy_ip.txt'
        with open(proxy_ip_filename, 'w') as f:
            f.write(text)
        text = open(proxy_ip_filename, 'r').read()
        proxy_ip_list = get_proxy_ip(text)
        print(proxy_ip_list)
    

获取如下数据：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306190326350.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)  
获取到代理IP地址后，发现数据缺失很多，再仔细查看elements，发现有些并非class = “odd”，而是…，这些数据没有被获取  
class = "odd"奇数的结果，而没有class = "odd"的是偶数的结果  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306190230123.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)  
通过bs4的find_all(‘tr’)来获取所有IP：

    
    
    def get_proxy_ip(response):
        proxy_ip_list = []
        soup = BeautifulSoup(response, 'html.parser')
        proxy_ips = soup.find(id = 'ip_list').find_all('tr')
        for proxy_ip in proxy_ips:
            if len(proxy_ip.select('td')) >=8:
                ip = proxy_ip.select('td')[1].text
                port = proxy_ip.select('td')[2].text
                protocol = proxy_ip.select('td')[5].text
                if protocol in ('HTTP','HTTPS','http','https'):
                    proxy_ip_list.append(f'{protocol}://{ip}:{port}')
        return proxy_ip_list
    

这次获得了80个代理IP地址：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306230813143.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)

#  使用代理

proxies的格式是一个字典：  
{‘http’: ‘ [ http://IP ](http://IP) :port‘,‘https’:' [ https://IP
](https://IP) :port‘}  
把它直接传入requests的get方法中即可  
web_data = requests.get(url, headers=headers, proxies=proxies)

    
    
    def open_url_using_proxy(url, proxy):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        headers = {'User-Agent': user_agent}
        proxies = {}
        if proxy.startswith('HTTPS'):
            proxies['https'] = proxy
        else:
            proxies['http'] = proxy
    
        try:
            r = requests.get(url, headers = headers, proxies = proxies, timeout = 10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return (r.text, r.status_code)
        except:
            print('无法访问网页' + url)
            return False
    url = 'http://www.baidu.com'
    text = open_url_using_proxy(url, proxy_ip_list[0])
    

#  确认代理IP地址有效性

无论是免费还是收费的代理网站，提供的代理IP都未必有效，我们应该验证一下，有效后，再放入我们的代理IP池中，以下通过几种方式：

  1. 访问网站，得到的返回码是200 

  2. 真正的访问某些网站，获取title等，验证title与预计的相同 

  3. 访问某些可以提供被访问IP的网站，类似于“查询我的IP”的网站，查看返回的IP地址是什么 

  4. 验证返回码 

    
    
    def check_proxy_avaliability(proxy):
        url = 'http://www.baidu.com'
        result = open_url_using_proxy(url, proxy)
        VALID_PROXY = False
        if result:
            text, status_code = result
            if status_code == 200:
                print('有效代理IP: ' + proxy)
            else:
                print('无效代理IP: ' + proxy)
    

大多是无效的！！！  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306205513508.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)

  2. 确认Title 

    
    
    def check_proxy_avaliability(proxy):
        url = 'http://www.baidu.com'
        text, status_code = open_url_using_proxy(url, proxy)
        VALID = False
        if status_code == 200:
            if r_title:
                if r_title[0] == '<title>百度一下，你就知道</title>':
                    VALID = True
        if VALID:
            print('有效代理IP: ' + proxy)
        else:
            print('无效代理IP: ' + proxy)
    

  3. 访问某些可以提供被访问IP的网站，类似于“查询我的IP”的网站，查看返回的IP地址是什么   
有很多这样的网站，比如（我找的大都是返回json的）：  
[ https://jsonip.com ](https://jsonip.com)  
[ https://api.myip.com ](https://api.myip.com)  
[ http://www.trackip.net/ip?json ](http://www.trackip.net/ip?json)  
[ https://api.ipify.org/?format=json ](https://api.ipify.org/?format=json)  
[ http://httpbin.org/ip,origin ](http://httpbin.org/ip,origin)  
[ https://ifconfig.co/json ](https://ifconfig.co/json)  
[ https://ip.seeip.org/jsonip ](https://ip.seeip.org/jsonip)  
[ https://ipapi.co/json/ ](https://ipapi.co/json/)  
[ http://www.geoplugin.net/json.gp ](http://www.geoplugin.net/json.gp)  
把经过测试可用的代理保存到文件（或数据库中），供今后使用  
完整代码：

    
    
    from bs4 import BeautifulSoup
    import requests
    import re
    import json
    
    
    def open_proxy_url(url):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        headers = {'User-Agent': user_agent}
        try:
            r = requests.get(url, headers = headers, timeout = 10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print('无法访问网页' + url)
    
    
    def get_proxy_ip(response):
        proxy_ip_list = []
        soup = BeautifulSoup(response, 'html.parser')
        proxy_ips = soup.find(id = 'ip_list').find_all('tr')
        for proxy_ip in proxy_ips:
            if len(proxy_ip.select('td')) >=8:
                ip = proxy_ip.select('td')[1].text
                port = proxy_ip.select('td')[2].text
                protocol = proxy_ip.select('td')[5].text
                if protocol in ('HTTP','HTTPS','http','https'):
                    proxy_ip_list.append(f'{protocol}://{ip}:{port}')
        return proxy_ip_list
    
    
    def open_url_using_proxy(url, proxy):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        headers = {'User-Agent': user_agent}
        proxies = {}
        if proxy.startswith(('HTTPS','https')):
            proxies['https'] = proxy
        else:
            proxies['http'] = proxy
    
        try:
            r = requests.get(url, headers = headers, proxies = proxies, timeout = 10)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return (r.text, r.status_code)
        except:
            print('无法访问网页' + url)
            print('无效代理IP: ' + proxy)
            return False
    
    
    def check_proxy_avaliability(proxy):
        url = 'http://www.baidu.com'
        result = open_url_using_proxy(url, proxy)
        VALID_PROXY = False
        if result:
            text, status_code = result
            if status_code == 200:
                r_title = re.findall('<title>.*</title>', text)
                if r_title:
                    if r_title[0] == '<title>百度一下，你就知道</title>':
                        VALID_PROXY = True
            if VALID_PROXY:
                check_ip_url = 'https://jsonip.com/'
                try:
                    text, status_code = open_url_using_proxy(check_ip_url, proxy)
                except:
                    return
    
                print('有效代理IP: ' + proxy)
                with open('valid_proxy_ip.txt','a') as f:
                    f.writelines(proxy)
                try:
                    source_ip = json.loads(text).get('ip')
                    print(f'源IP地址为：{source_ip}')
                    print('='*40)
                except:
                    print('返回的非json,无法解析')
                    print(text)
        else:
            print('无效代理IP: ' + proxy)
    
    
    if __name__ == '__main__':
        proxy_url = 'https://www.xicidaili.com/'
        proxy_ip_filename = 'proxy_ip.txt'
        #  text = open_proxy_url(proxy_url)
        #  with open(proxy_ip_filename, 'w') as f:
            #  f.write(text)
        text = open(proxy_ip_filename, 'r').read()
        proxy_ip_list = get_proxy_ip(text)
        proxy_ip_list.insert(0, 'http://172.16.160.1:3128') #我自己的代理服务器
        for proxy in proxy_ip_list:
            check_proxy_avaliability(proxy)
    
    

以下是测试结果： ![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306214547113.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)  
真正可用的代理IP只有14个：  
![!\[在这里插入图片描述\]\(https://img-blog.csdnimg.cn/20190306214846733.png](https://img-blog.csdnimg.cn/20190306230416718.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)

#  关于http和https代理

可以看到proxies中有两个键值对：  
{‘http’: ‘ [ http://IP ](http://IP) :port‘,‘https’:' [ https://IP
](https://IP) :port‘}  
其中 HTTP 代理，只代理 HTTP 网站，对于 HTTPS 的网站不起作用，也就是说，用的是本机 IP，反之亦然。  
我刚才使用的验证的网站是https://jsonip.com, 是HTTPS网站  
所以探测到的有效代理中，如果是https代理，则返回的是代理地址  
如果是http代理，将使用本机IP进行访问，返回的是我的公网IP地址  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190306221543674.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzcyMDM5Ng==,size_16,color_FFFFFF,t_70)

#  使用的有用户名和密码认证的代理

如果买的是付费代理，比如阿布云一般会提供用户名和密码进行认证，可以使用以下代码把认证信息放到代码中：

    
    
    def get_proxies():
        # 代理服务器
        proxyHost = "http-dyn.abuyun.com"
        proxyPort = "9020"
    
        # 代理隧道验证信息
        proxyUser = "proxyuser"
        proxyPass = "proxyPass"
    
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
          "host" : proxyHost,
          "port" : proxyPort,
          "user" : proxyUser,
          "pass" : proxyPass,
        }
        proxies = {
            "http"  : proxyMeta,
            "https" : proxyMeta,
        }
    

