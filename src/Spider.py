# coding=utf-8

from __future__ import unicode_literals  # 解决json.dumps的中文乱码问题
import json
import os
import re  # 正则
import time
from urllib import request
import config
import requests
import random

# itemid = config.itemid
itemid_list = config.itemid_list
file_path = config.file_path


def get_random_ip(proxy_list):
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': 'http://' + proxy_ip.rstrip('\n'),
               'https': 'https://' + proxy_ip.rstrip('\n')}
    return proxies


def getRawData(file_path, raw_data, itemid):
    f_proxy = open('proxy.txt', 'r+')
    proxy_list = f_proxy.readlines()
    f_proxy.close()

    headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/63.0',
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    }
    current_page = 1
    err_page = []
    proxies = get_random_ip(proxy_list)

    while 1:
        try:
            print('正在抓取第{}页\n'.format(current_page))
            url = ('https://rate.taobao.com/feedRateList.htm?auctionNumId=' +
                   itemid + '&currentPageNum={}').format(current_page)
            byte = requests.get(url, headers=headers,
                                proxies=proxies, timeout=10)
            string = byte._content.decode('UTF-8')

            string = re.sub('[\r\t\n]', '', string)
            string = string.strip(')')
            string = string.strip('(')
            response_json = json.loads(string)
            max_page = response_json['maxPage']
            raw_data.append(string)

        except Exception as err:
            print('抓取第{}页出现问题:'.format(current_page) + str(err))
            err_page.append(current_page)
            proxies = get_random_ip(proxy_list)
            continue

        current_page = current_page + 1
        if (current_page > max_page):
            break
        time.sleep(1)

    print('抓取完毕\n')
    if any(err_page):
        print('抓取第{}页出现问题\n'.format(err_page))


def main():
    for itemid in itemid_list:
        if not os.path.exists(file_path + itemid):
            os.makedirs(file_path + itemid)

        raw_data = list()
        getRawData(file_path, raw_data, itemid)

        f = open(file_path + itemid + '/' +
                 'raw_data.txt', 'w', encoding='UTF-8')
        for line in raw_data:
            f.write(line+'\n')
        f.close()


if __name__ == '__main__':
    main()
