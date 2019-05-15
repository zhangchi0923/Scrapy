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
    proxy_ips = soup.find(id = 'ip_list').find_all('tr') # ip_list是table的id值，定位到IP表后检索tr（即表格内容）中的所有内容
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

    print(count)