# coding=utf-8

from __future__ import unicode_literals  # 解决json.dumps的中文乱码问题
import json
import os
import re  # 正则
import time
import math
import decimal
from urllib import request
import config

itemid = config.itemid
file_path = config.file_path

dic_l1 = ['外观', '样子', '漂亮', '塑料', '金属', '光泽', '按键', '显示屏', '大屏',
          '不锈钢', '廉价', '样式', '空间', '大小', '容量', '高大上', '档次', '大方']
dic_l2 = ['滚筒', '波轮', '洗烘一体', '迷你', '半自动', '全自动', '自动', '变频', '静音', '安全', '脱水',
          '功能', '甩干', '提示音', '公斤', '省水', '干净', '噪音', '声音', '不平', '震动', '振动', '效果']
dic_l3 = ['预约', '消毒', '儿童锁', '程序', '免清洗', '除菌', '称重', '能效',
          '洗衣液', 'WiFi', '智能', '控制', '烘干', '节能', '高温', '变频', '温水', '省电']
dic_l4 = ['上门', '安装', '师傅', '预约', '工人', '泡沫', '包装', '送货',
          '扛', '调试', '专业', '免费', '收费', '讲解', '约定', '速度', '神速']
dic_l5 = ['满意', '性价比', '服务', '售前', '售后', '物美价廉', '值得', '不值',
          '实体店', '旗舰店', '下次', '质量', '划算', '耐心', '赠品', '品牌', '方便']

state_word = ['啊', '哇', '哎', '唉', '呀', '哈']
punctuation = ['？', '！', '……']

attr_words = []
opin_words = []


def getAttrAndOpin():
    try:
        f_attr = open(file_path + itemid + '/attr.txt', 'r', encoding='UTF-8')
        f_opin = open(file_path + itemid + '/opin.txt', 'r', encoding='UTF-8')
    except Exception as err:
        print(err)
        return

    attr_words = f_attr.readlines()
    opin_words = f_opin.readlines()
    f_attr.close()
    f_opin.close()

    for i in range(0, len(attr_words)):
        attr_words[i] = attr_words[i].replace('\n', '')
    for i in range(0, len(opin_words)):
        opin_words[i] = opin_words[i].replace('\n', '')


def getKeywordNumofComment(comment, dic_key_word):
    n = 0
    for item in dic_key_word:
        n += comment.count(item)
    return n


def getTotalUsefulNum(comments):
    useful = 0
    for item in comments:
        useful += item['useful']
    return useful


def getH2(useful_num, useful_total_num, param=1.2):
    if useful_num == 0:
        return 0

    H2 = 0
    if useful_num > 0 and useful_num <= 3:
        H2 = useful_num / useful_total_num
    elif useful_num > 3:
        H2 = (useful_num / useful_total_num) * param
    else:
        H2 = 0

    if H2 > 1:
        return 1
    else:
        return H2

# 评论中最早的时间和当条评论日期差


def getH3(comment_timestamp, most_early_comment_date):
    return comment_timestamp/86400 - most_early_comment_date/86400

# TODO:加入情感词关键词


def getH4(comment, comment_len):
    if comment_len <= 10:
        return 1
    elif comment_len > 10 and comment_len <= 39:
        return 2
    elif comment_len >= 40 and comment_len <= 59:
        return 3
    elif comment_len >= 60 and comment_len <= 99:
        return 2
    elif comment_len >= 100:
        return 1
    # n1 = getKeywordNumofComment(comment, state_word)
    # n2 = getKeywordNumofComment(comment, punctuation)
    # if 0 == n1 or 0 == n2:
    #     return 0

    # return (math.log10(n1 + n2) / math.log10(n1))


def getH5(pic_num):
    if pic_num <= 0:
        return 1
    if pic_num >= 1 and pic_num <= 3:
        return 2
    if pic_num >= 4 and pic_num < 7:
        return 3
    if pic_num >= 7:
        return 4


# 属性词匹配加1分
def getD1(comment):
    return getKeywordNumofComment(comment, attr_words)  # / k_max


# 观点词匹配加1分
def getD2(comment):
    return getKeywordNumofComment(comment, opin_words)


def main():
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)

    getAttrAndOpin()

    f_output = open(file_path + itemid + '/output.txt', 'w', encoding='UTF-8')
    f_content = open(file_path+itemid+'/content.txt', 'w', encoding='UTF-8')
    f_scores = open(file_path+itemid+'/scores.txt', 'w', encoding='UTF-8')
    try:
        f_raw_data = open(file_path + itemid +
                          '/raw_data.txt', 'r', encoding='UTF-8')
    except Exception as err:
        print(err)
        return

    comments = list()
    for line in f_raw_data:
        raw_data_json = json.loads(line)
        comments += raw_data_json['comments']

    useful_total_num = getTotalUsefulNum(comments)

    for each in comments:
        user_name = each['user']['nick']
        user_viplevel = each['user']['vipLevel']
        user_rank = each['user']['rank']
        content = each['content']
        # if ('此用户没有填写评价' not in content) and len(content)<256:
        #     f_content.write(content+'。')
        f_content.write(content+'\n')
        date = each['date'].replace(
            '年', '-').replace('月', '-').replace('日', '')
        date = date[:10]
        if len(date) != 0:
            timestamp = time.mktime(time.strptime(date, '%Y-%m-%d'))
            if most_early_comment_date > timestamp:
                most_early_comment_date = timestamp
        else:
            timestamp = 0

        pic_num = len(each['photos'])
        useful = each['useful']
        f_output.write('用户名：' + user_name + '\t')
        f_output.write('VIP等级：' + str(user_viplevel) + '\t')
        f_output.write('用户等级：'+str(user_rank)+'\t')
        f_output.write('评论：'+content+'\t')
        f_output.write('时间：' + date + '\t')
        f_output.write('图片数：' + str(pic_num) + '\t')
        f_output.write('点赞数：' + str(useful) + '\t')

        append_comment = each['appendList']
        if any(append_comment):
            append_comment = append_comment[0]
            append_content = append_comment['content']
            # if ('此用户没有填写评价' not in append_content)and len(append_content)<256:
            #     f_content.write(append_content+'。')
            append_time = append_comment['dayAfterConfirm']
            append_pic_num = len(append_comment['photos'])
            f_output.write('追评：'+append_content+'\t')
            f_output.write('追评时间：'+str(append_time)+' 天后'+'\t')
            f_output.write('追评图片数：' + str(append_pic_num) + '\t')

        H2 = getH2(useful, useful_total_num)
        H3 = getH3(timestamp, most_early_comment_date)
        H4 = getH4(content, len(content))
        H5 = getH5(pic_num)
        D1 = getD1(content)
        D2 = getD2(content)

        f_scores.write(str(decimal.Decimal(H4).quantize(
            decimal.Decimal('0.00'))) + '\t')
        f_scores.write(str(decimal.Decimal(H3).quantize(
            decimal.Decimal('0.00'))) + '\t')
        f_scores.write(str(decimal.Decimal(H2).quantize(
            decimal.Decimal('0.00'))) + '\t')
        f_scores.write(str(decimal.Decimal(H5).quantize(
            decimal.Decimal('0.00'))) + '\t')
        f_scores.write(str(decimal.Decimal(D1).quantize(
            decimal.Decimal('0.00'))) + '\t')
        f_scores.write(str(decimal.Decimal(D2).quantize(
            decimal.Decimal('0.00'))) + '\t')

        f_scores.write('\n')

    f_scores.close()


if __name__ == '__main__':
    main()
