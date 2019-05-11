import requests


#get请求

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
try:
    response = requests.get("http://www.baidu.com/",headers = headers)
except requests.HTTPError as e:
    # print(response.text)
     print(response.status_code)

#post请求
formdata = {'form_email':'1099327299@qq.com','form_password':'stayin1302@'}
response = requests.post('http://www.douban.com/login',formdata)
print (response.text)

