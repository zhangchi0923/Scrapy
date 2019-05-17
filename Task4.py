# -*- coding: UTF-8 -*- requests
import requests
from selenium import webdriver
import time
from lxml import etree

class Login_Scrap():

    def __init__(self,url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        time.sleep(2)
    # 登陆
    def login(self,username,password):

        # 按照html标签定位"返回电脑登陆"按钮
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/a[2]').click()
        input_name = self.driver.find_element_by_name('username')  # 找到用户名输入框
        input_name.send_keys(username)  # 输入自己用户名
        input_password = self.driver.find_element_by_name('password')  # 找到密码输入框
        input_password.send_keys(password)  # 输入自己的邮箱密码
        # 按照标签定位"登录"按钮
        self.driver.find_element_by_xpath('//*[@id="user"]/div[1]/div[3]/button').click()  # 点击登陆按钮
        time.sleep(10)
        # 已经提交的用户信息会保存到cookie中
        cookie = self.driver.get_cookies()
        cookie_dict = {i['name']: i['value'] for i in cookie}
        return cookie_dict

    def getContent(self,url,username,password):
        cookies = self.login(username,password)
        hd = {'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) "}
        r = requests.get(url, headers = hd, cookies = cookies,timeout = 10)
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        users = html.xpath('//div[@class="auth"]')
        times = html.xpath('//div[@class="post-info"]/span')
        contents = html.xpath('//td[@class="postbody"]')
        for i in range(len(users)):
            user = users[i].xpath('string(.)').encode('utf-8')
            time = times[i]
            content = contents[i].xpath('string(.)').strip().encode('utf-8')
            print('user: '+ user)
            print('post time: '+ time)
            print('content: '+content)


if __name__ == "__main__":
    url = 'https://auth.dxy.cn/accounts/login?service=http://www.dxy.cn/bbs/thread/626626'
    usrnm = '1099327299@qq.com'
    pw = 'password'
    # Login_Scrap(url).login(usrnm,pw)
    Login_Scrap(url).getContent(url,usrnm,pw)