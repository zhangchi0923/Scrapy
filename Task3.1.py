# -*- coding: utf-8 -*-
from selenium import webdriver
import time


class Login():
    # 构造器中启动Chrome浏览器并获取页面，等待5s
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://mail.163.com/")
        time.sleep(5)
    def login(self,username,pw):
        # 无法用id获取登陆框，这里只能用switch指向
        self.driver.switch_to.frame(0)
        # 找到邮箱和密码的输入框并输入相应信息
        inputText = self.driver.find_element_by_name('email')
        inputText.send_keys(username)
        password = self.driver.find_element_by_name('password')
        password.send_keys(pw)
        # 定位登陆按钮并点击，等待10s，成功登陆后退出浏览器
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
    password = "stayin1302@"
    Login().login(username,password)