## python爬虫（三）

#### 3.1 Selenium

Selenium是一款用于浏览器自动化测试的工具。我们这里主要使用WebDriver。

- find_element方法

  ​	WebDriver的find_element方法用于定位元素，selenium提供了8种元素定位：id, class, name, tag, link, partail_link, xpath, css. 实际使用中，我们通过找到相应的元素来进行信息的获取、提交或者页面操作。  

  ​	登陆163邮箱的步骤：

  （1）启动浏览器并来到登陆页面

  （2）定位到登录框

  （3）定位到账户输入框和密码输入框，输入相应信息

  （4）定位"登陆"按钮，并点击

后两个步骤涉及到了对元素的操作，会用到WebElement。

- send_keys方法

  ​	send_keys方法模拟键盘输入，我们要将邮箱和密码输入进去。

  ```python
  inputText = self.driver.find_element_by_name('email')
  inputText.send_keys(username)
  ```

- click方法模拟鼠标点击，输入信息后点击"登陆"按钮。

  ```
  login_em = self.driver.find_element_by_id('dologin')
  login_em.click()
  ```

  

代码实现：

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time


class Login():
    # (1)构造器中启动Chrome浏览器并获取页面，等待5s
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://mail.163.com/")
        time.sleep(5)
    def login(self,username,pw):
        # (2)无法用id获取登陆框，这里只能用switch指向
        self.driver.switch_to.frame(0)
        # (3)找到邮箱和密码的输入框并输入相应信息
        inputText = self.driver.find_element_by_name('email')
        inputText.send_keys(username)
        password = self.driver.find_element_by_name('password')
        password.send_keys(pw)
        # (4)定位登陆按钮并点击，等待10s，成功登陆后退出浏览器
        login_em = self.driver.find_element_by_id('dologin')
        login_em.click()
        time.sleep(10)
        self.driver.quit()
    def logout(self):
        self.driver.find_element_by_link_text('退出').click()
        time.sleep(5)

# 主程序
if __name__ == "__main__":
    username = "18840830137@163.com"
    password = "yourpassword"
    Login().login(username,password)
```

<p><img src="/163登陆成功.png" alt="好像暂时显示不出来..." width="304" height="228"/></p>

也可基于上述代码实现在百度首页检索关键字以及在首页点击进入"视频板块"并检索关键字：

```python
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

class KeyWordSearch():

    def __init__(self,url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        time.sleep(1)
    def searchResults(self, kw):
        # 下面这段代码是在百度首页键入关键字检索
        # input = self.driver.find_element_by_id("kw")
        # input.send_keys(kw)
        # 点击"视频"，进入百度视频首页
        button = self.driver.find_element_by_name("tj_trvideo")
        button.click()
        # 点击视频检索框并键入关键字
        input = self.driver.find_element_by_id("new-bdvSearchInput")
        input.send_keys(kw)
        # 点击"百度一下"按钮
        button2 = self.driver.find_element_by_id("new-bdvSearchBtn")
        button2.click()
        wait = WebDriverWait(self.driver,5)
        print(self.driver.current_url)
        # print(self.driver.page_source)
        time.sleep(20)
        self.driver.quit()


url = "http://www.baidu.com"
kw = "奥巴梅扬"

if __name__ == "__main__":
    KeyWordSearch(url).searchResults(kw)
```

<p><img src="/搜索奥巴梅扬视频.png" alt="好像暂时显示不出来..." width="304" height="228"/></p>

#### 3.2 使用代理访问

​	在网络中，各个终端互相通信时需要为每一个终端制定一个唯一的标识（地址），这就是ip地址。常见的IPV4地址有四个网段组成，每个网段由一个0-255的十进制数字构成。

​	当我们用同一个ip访问某一网站的频率过高时，该网站可能会封掉我们使用的ip。我们有两种方式应对：降低访问频率；找到合适的代理不断更换再去访问该网站。这节介绍如何建立自己的代理池。

##### 思路

（1）从 https://www.xicidaili.com/ 上爬取提供的代理ip

（2）将每个ip组装成url

（3）测试每个proxy是否好用（检查status_code和title内容）

```python
from bs4 import BeautifulSoup
import requests
import re

def open_proxy_url(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    headers = {'User-Agent': user_agent}
    try:
        r = requests.get(url, headers = headers, timeout = 20)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('无法访问网页' + url)


def get_proxy_ip(response):
    all_proxy_ip_url = 'proxy_ip_url_list.txt'
    proxy_ip_list = []
    soup = BeautifulSoup(response, 'html.parser')
    proxy_ips = soup.find(id = 'ip_list').find_all('tr') 
    # ip_list是table的id值，定位到IP表后检索tr（即表格内容）中的所有内容
    for proxy_ip in proxy_ips:
        content = proxy_ip.select('td')
        if len(content) >=8:
            ip = content[1].text        # 对应ip地址
            port = content[2].text      # 对应端口号
            protocol = content[5].text  # 对应协议名称
            if protocol in ('HTTP','HTTPS','http','https'):
                proxy_ip_list.append('{0}://{1}:{2}'.format(protocol,ip,port))
    return proxy_ip_list

def check_proxy_ip(url, ip):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    headers = {'User-Agent': user_agent}
    proxy = {}
    FLAG = False
    if ip.startswith('HTTPS'):
        proxy['https'] = ip
    else:
        proxy['http'] = ip

    try:
        r = requests.get(url,headers = headers,proxies = proxy,timeout = 15)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        # 检查status_code和title内容
        if r.status_code == 200:
            r_title = re.findall('<title>.*</title>',r.text)
            if r_title:
                if r_title[0] == '<title>百度一下，你就知道</title>':
                    print(ip)
                    FLAG = True
        if FLAG == True:
            # 将能用的代理ip写入txt文件
            with open('good_ip.txt', 'a') as f:
                f.writelines(ip+"\n")
    except:
        print('proxy : {} is not available'.format(ip))
    return FLAG

if __name__ == '__main__':
    proxy_url = 'https://www.xicidaili.com/'
    url = 'https://www.baidu.com'
    count = 0
    text = open_proxy_url(proxy_url)
    proxy_ip_filename = 'proxy_ip.txt'
    proxy_ip_list = get_proxy_ip(text)
    for proxy_ip in proxy_ip_list:
        if check_proxy_ip(url,proxy_ip):
            count += 1

    print(count)# 打印能用的代理个数
```

<div><img src="/p1.png" alt="好像暂时显示不出来..." width="304" height="228"/></div><div><img src="/p2.png" alt="好像暂时显示不出来..." width="304" height="228"/></div>

