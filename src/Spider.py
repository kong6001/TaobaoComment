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
    if len(proxy_list) == 0:
        return None
    proxy_ip = random.choice(proxy_list)
    proxy_list.remove(proxy_ip)
    proxies = {'http': 'http://' + proxy_ip.rstrip('\n'),
               'https': 'https://' + proxy_ip.rstrip('\n')}
    return proxies


def getRawData(file_path, raw_data, itemid):
    f_proxy = open('proxy.txt', 'r+')
    proxy_list = f_proxy.readlines()
    f_proxy.close()

    #每次爬取前要更换cookie
    headers = {
        "Host": "rate.taobao.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://item.taobao.com/item.htm?spm=a230r.1.14.69.1e11156blW6cwp&id=546948347981&ns=1&abbucket=12",
        "Connection": "keep-alive",
        "Cookie": "isg=BFJSDqTmWhZz46Cwck-YnSPJoBj0y1fjJiCT4hyrCoXLL_MpBPFrDBWFn0u2RM6V; cna=VSwoEy9S4joCAXAKVA0fo5Yn; enc=OoIgjbduPNUiTI6fxwC38TBD869LbJ9vVvVfjvBLBwzh%2BxrFfzxWE1tKrvibEKZaoXDKix5S7mLRXiE68Pm5sg%3D%3D; um=G1548C82116B16BD820881C7D5E4BAA5603519F; _cc_=UIHiLt3xSw%3D%3D; tg=0; miid=7157687411736942446; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; l=bBNswcYVvSQK0PbbBOCwVuI8Lq_9kIObYuPRwCXwi_5N418CfaQOlF0A8eJ6Vs5PO6YB4KXJ7LptuFng-yW1.; t=2150bc9b756be7147858039a105889c7; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; _m_h5_tk=dc69a685f2c90386deeae08f64ccd263_1560005725771; _m_h5_tk_enc=b7943b76674131181890f5d8c823e3d1; mt=ci=0_0; cookie2=55eceab93c2609c03121e01205debb04; _tb_token_=53551b66841ae; swfstore=246891; whl=-1%260%260%261559985074709; JSESSIONID=7A72618EE39D89CDAD8DC7693C2B2AE8; v=0; x5sec=7b22726174656d616e616765723b32223a226533373631643836333039366635376331373461636135383439626131363738434a2b57372b6346454979516f384b32734e716453513d3d227d",
        "TE": "Trailers"
    }

    current_page = 1
    err_page = []
    proxies = get_random_ip(proxy_list)

    while 1:
        try:
            print('正在抓取第{}页\n'.format(current_page))
            # url = ("https://rate.tmall.com/list_detail_rate.htm?itemId=" + itemid +
                #    "&spuId=946472412&sellerId=2943953365&order=3&currentPage={}&append=0&content=1&tagId=&posi=&picture=&groupId=&ua=098").format(current_page)
            url = ('https://rate.taobao.com/feedRateList.htm?auctionNumId=' +
               itemid + '&currentPageNum={}').format(current_page)
            byte = requests.get(url, headers=headers,
                                proxies=proxies,
                                timeout=10)
            string = byte._content.decode('UTF-8')

            string = re.sub('[\r\t\n]', '', string)
            string = string.strip(')').strip(
                '(').strip('jsonp128').strip("jsonp_tbcrate_reviews_list").strip(')').strip('(')
            response_json = json.loads(string)
            max_page = 0
            if "maxPage" in response_json:
                max_page = response_json['maxPage']
            elif "rateDetail" in response_json:
                max_page = response_json["rateDetail"]["paginator"]['lastPage']
            else:
                max_page = response_json["throw"]

            raw_data.append(string)

        except Exception as err:
            print('抓取第{}页出现问题:'.format(current_page) + str(err))
            err_page.append(current_page)
            proxies = get_random_ip(proxy_list)
            if proxies == None:
                break
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
