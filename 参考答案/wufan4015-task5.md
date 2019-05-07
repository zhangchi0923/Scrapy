---
title: Python爬虫学习-Day5
date: 2019-03-05 21:02:11
tags: ['selenium安装', '163邮箱模拟登陆']
categories: ['selenium安装', '163邮箱模拟登陆']
copyright: true
---
###  1、安装selenium

昨晚在mac中安装出现问题，今天在win10中实验了下，还给鼓捣成功了，下面来说说安装时碰到的坑。

  * 安装chromedriver 

首先https://sites.google.com/a/chromium.org/chromedriver/downloads已经不能登陆下载了，重新找了一个http://npm.taobao.org/mirrors/chromedriver/，在下载时先要确定自己的chrome的版本号，我的版本是72.0.3626，在浏览器的帮助/关于chrome可以看到。  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305121848550.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)  
安装的chromedriver版本如下，没有对应win64的版本，所以就下个32位的。  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305121939239.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)  
然后将.exe文件放到chrome的安装文件中，chrome安装路径我的是：C:\Users\fg\AppData\Local\Google\Chrome，可以在桌面选中chrome右击打开文件位置来找。放好后将这个路径添加到环境变量中，win10的话直接搜索环境变量如下：  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305122605620.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)  
打开后选择环境变量打开  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305122649868.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)  
然后选择path打开，注意是系统变量的path，然后添加进去就ok了。  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305123000823.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)

  * 安装selenium   
安装比较方便，直接pip install selenium就好了。  
在安装时要注意，如果电脑上有多个版本python（比如python3.x、python2.x、anaconda自带的python等等）要选对pip来安装，我由于工作需要，python3版本有64位跟32位，还有anaconda的python，所以直接用pip
install selenium安装会默认安装到python3的64位中。  
由于平常一直都是用的anaconda，所以又在anaconda中安装了下，我的方法是pip show
selenium找到刚才安装的库路径：c:\users\fg\appdata\local\programs\python\python64\lib
\site-packages  
然后直接找到selenium库的文件夹cope到anaconda安装目录中C:\Users\fg\Anaconda3\Lib\site-
packages文件夹下。

  * 试用selenium 

    
    
    from selenium import webdriver
    
    browser = webdriver.Chrome()
    browser.get("http://www.baidu.com")
    
    结果：
    runfile('G:/新建文件夹/大数据/spyder_test/selenium_TEST.py', wdir='G:/新建文件夹/大数据/spyder_test')
    

会弹出chrome的窗口，并显示chrome正受到自动测试软件的控制。  
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305124108329.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)

###  2、利用selenium登陆163邮箱

    
    
    import time
    from selenium import webdriver
    #from selenium.webdriver.common.keys import Keys
    
    
    browser = webdriver.Chrome()
    url = 'http://mail.163.com/'
    browser.get(url)
    time.sleep(3)
    
    browser.maximize_window()#打开网页窗口
    
    time.sleep(5)
    
    browser.switch_to.frame(0)#找到邮箱账号登录框对应的iframe,由于网页中iframe的id是动态的，所以不能用id寻找
    
    email = browser.find_element_by_name('email')#找到邮箱账号输入框
    
    email.send_keys('13265923587@163.com')#将自己的邮箱地址输入到邮箱账号框中
        
    password = browser.find_element_by_name('password')#找到密码输入框
        
    password.send_keys('******')#输入自己的邮箱密码
        
    login_em = browser.find_element_by_id('dologin')#找到登陆按钮
        
    login_em.click()#点击登陆按钮
          
    time.sleep(10)
    

总结：

  * 在安装selenium时遇到一些问题，mac配置环境不成功，改用win操作，还需研究mac的配置。 
  * 在登陆邮箱时，切换如iframe时，开始未注意到id是动态的，一直报错，后来尝试了一些方法后成功登陆。 
  * 更新：mac已配置成功，问题出在配置好环境变量了，但是未加入anaconda中，详细的操作如下 
  * 将下载的chromedrive移到anaconda下对应的bin目录中，如：anaconda3/bin中。然后在终端运行sudo easy_install selenium，出现如下提示就大功告成了。   
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190305235138460.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MjkzNzM4NQ==,size_16,color_FFFFFF,t_70)

