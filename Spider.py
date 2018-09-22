# coding=utf-8

from __future__ import unicode_literals  # 解决json.dumps的中文乱码问题
import json
import os
import re  # 正则
import time
from urllib import request
import config

itemid = config.itemid
file_path = config.file_path


def getRawData(file_path, raw_data):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.37'
    }

    current_page = 1
    err_page = []

    while 1:
        try:
            print('正在抓取第{}页\n'.format(current_page))
            url = ('https://rate.taobao.com/feedRateList.htm?auctionNumId=' +
                   itemid + '&currentPageNum={}').format(current_page)
            res = request.Request(url, method='GET', headers=headers)
            byte = request.urlopen(res).read()
            string = byte.decode('UTF-8')

            string = re.sub('[\r\t\n]', '', string)
            string = string.strip(')')
            string = string.strip('(')
            response_json = json.loads(string)
            max_page = response_json['maxPage']
            raw_data.append(string)

        except Exception as err:
            print('抓取第{}页出现问题:'.format(current_page) + str(err))
            err_page.append(current_page)
            continue

        current_page = current_page+1
        if (current_page > max_page):
            break

    print('抓取完毕\n')
    if any(err_page):
        print('抓取第{}页出现问题\n'.format(err_page))


def main():
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)

    raw_data = list()
    getRawData(file_path, raw_data)

    f = open(file_path + itemid + '/' +
             'raw_data.txt', 'w', encoding='UTF-8')
    for line in raw_data:
        f.write(line+'\n')
    f.close()


if __name__ == '__main__':
    main()
