import requests


#get请求
hd = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()            #如果状态不是200，则引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Exception!"


if __name__ == "__main__":
    url = "http://www.baidu.com"
    print(getHTMLText(url))




