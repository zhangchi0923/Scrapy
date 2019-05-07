---
title: 模拟登录丁香园，并抓取论坛页面所有的人员基本信息与回复帖子内容
date: 2019-03-07 18:41:00
tags: []
categories: []
copyright: true
---
丁香园直通车 [ 抓取页面链接 ](http://www.dxy.cn/bbs/thread/626626#626626)  
一.首先利用selenium登录网站，此部分重点：  
1.切换到账号密码表单登录，我采用了利用style将display值变为block，代码如下：

    
    
    		js1 = 'document.querySelector("#j_loginTab1").style.display="none";'
    		browser.execute_script(js1)
    		time.sleep(1)
    		js2 = 'document.querySelector("#j_loginTab2").style.display="block";'
    		browser.execute_script(js2)
    

2.定位到账号，密码input位置并输入已注册好的帐号密码，点击登录，代码如下：

    
    
    		input_name = browser.find_element_by_name('username')
    		input_name.clear()
    		input_name.send_keys(********')
    		input_pass = browser.find_element_by_name('password')
    		input_pass.clear()
    		input_pass.send_keys('********')
    		browser.find_element_by_xpath('//*[@class="form__button"]/button').click()
    

**此步骤操作多了会出现验证，验证方式我遇到过按顺序点击图片中的汉字、滑动图片块等；本文先跳过，后期补上这一部分。**  
3.登录成功后，我们开始抓取页面，利用xpath定位到抓取内容的位置；

    
    
    		user = tree.xpath('//div[@id="postcontainer"]//div[@class="auth"]/a/text()')
    		content = tree.xpath('//td[@class="postbody"]')
    

4.将抓取内容存入文件。  
整体代码如下

    
    
    # -*- coding:utf-8 -*-
    import requests, json, re, random,time
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from lxml import etree
    
    class getUrl(object):
    	"""docstring for getUrl"""
    	def __init__(self):
    		self.headers={
                "Connection": "keep-alive",  
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "  
                              "(KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36",  
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  
                "Accept-Encoding": "gzip, deflate, sdch",  
                "Accept-Language": "zh-CN,zh;q=0.8"
            };
    
    	def run(self):
    		browser = webdriver.Chrome()
    		browser.get('https://auth.dxy.cn/accounts/login?service=http://www.dxy.cn/bbs/index.html')
    		time.sleep(1)
    		#切换账号密码登录表单
    		js1 = 'document.querySelector("#j_loginTab1").style.display="none";'
    		browser.execute_script(js1)
    		time.sleep(1)
    		js2 = 'document.querySelector("#j_loginTab2").style.display="block";'
    		browser.execute_script(js2)
    		#输入账号密码
    		input_name = browser.find_element_by_name('username')
    		input_name.clear()
    		input_name.send_keys('*********')
    		input_pass = browser.find_element_by_name('password')
    		input_pass.clear()
    		input_pass.send_keys('*******')
    		browser.find_element_by_xpath('//*[@class="form__button"]/button').click()
    		#此步骤应该有验证码，先跳过
    		time.sleep(10)
    		cookie = browser.get_cookies()
    		cookie_dict = {i['name']:i['value'] for i in cookie}
    		#转到抓取页面
    		browser.get("http://www.dxy.cn/bbs/thread/626626#626626"); 
    		html = browser.page_source
    		tree = etree.HTML(html)
    		user = tree.xpath('//div[@id="postcontainer"]//div[@class="auth"]/a/text()')
    		content = tree.xpath('//td[@class="postbody"]')
    		for i in range(0,len(user)):
    			result = user[i].strip()+":"+content[i].xpath('string(.)').strip()
    			#写入文件
    			dir_file = open("DXY_records.txt",'a', encoding="utf-8")
    			dir_file.write(result+"\n")
    			dir_file.write('*' * 80+"\n")
    			dir_file.close()
    		print('*' * 5 +"抓取结束"+'*' * 5)
    
    
    if __name__ == '__main__':
    	geturl = getUrl()
    	geturl.run()
    

**运行结果如下，一共有27个用户回复(此代码只适用于回复只有单页的情况，若是有多页回复，需在获取页面html代码处加入循环，依次抓取)**  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190307184025117.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L25hb25hbzc3,size_16,color_FFFFFF,t_70)

