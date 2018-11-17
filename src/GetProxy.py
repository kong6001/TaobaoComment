# encoding=utf8

# 获取代理IP
from bs4 import BeautifulSoup
import requests
import urllib
import socket

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url = 'http://www.xicidaili.com/nn/1'
ack = requests.get(url, headers=header)
res = ack._content.decode('UTF-8')

soup = BeautifulSoup(res)
ips = soup.findAll('tr')
f = open("proxy.txt", "w+")

lines = []
for x in range(1, len(ips)):
    ip = ips[x]
    tds = ip.findAll("td")
    ip_port = tds[1].contents[0] + ":" + tds[2].contents[0]
    lines.append(ip_port)

for i in range(0, len(lines)):
    ip_port = lines[i]
    proxy_host = "http://" + ip_port
    proxy = {"http": proxy_host}

    try:
        s = requests.session()
        s.proxies = proxy
        res = s.get(url, timeout=3)
        print(ip_port)
        f.write(ip_port+'\n')
    except Exception as e:
        # print(proxy)
        # print(e)
        continue
