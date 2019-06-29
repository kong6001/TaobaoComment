# coding=GBK

from __future__ import unicode_literals  # 解决json.dumps的中文乱码问题

import decimal
import json
import math
import os
import re  # 正则
import time
from urllib import request

import jieba

import config

len_avg = config.len_avg
len_variance = config.len_variance
weight_list = [0.157, 0.095, 0.165,0.093,0.164,0.185, 0.141]


levelwords = [config.level1words, config.level2words, config.level3words, config.level4words]
feelwords = []
file_list = os.listdir('feelwords')
for file in file_list:
    f = open('feelwords/' + file, 'r+', encoding='GBK')
    words = f.readlines()
    for word in words:
        if word != "\n":
            feelwords.append(word.strip())

owords = set(config.wo1)
owords=owords|set(config.wo2)
owords=owords|set(config.wo3)
owords=owords|set(config.wo4)
owords=owords|set(config.wo5)


#可信度
def getCredibilityScore(user_name, rank):
    score=0
    if '**' in user_name:
        score+= 0
    else:
        score += 0.5

    if rank >= 5000:
        score += 1
    elif rank < 5000 and rank >= 2000:
        score += 0.9
    elif rank < 2000 and rank >=1000:
        score += 0.8
    elif rank < 1000 and rank >=500:
        score += 0.7
    elif rank < 500 and rank >=250:
        score += 0.6
    elif rank < 250 and rank >=150:
        score += 0.5
    elif rank < 150 and rank >=90:
        score += 0.4
    elif rank < 90 and rank >=40:
        score += 0.3
    elif rank < 40 and rank >=10:
        score += 0.2
    elif rank < 10 and rank >=4:
        score += 0.1
    elif rank < 4:
        score += 0

    if score > 1:
        score = 1
        
    return score


#时效性
def getTimelinessScore(time_stamp, most_early_timestamp):
    today_timestamp = time.time()
    delta_date = (today_timestamp - time_stamp) / 60 / 60 / 24
    ret = (360 - delta_date) / 10
    if ret < 0:
        ret = 0
    return ret


#阅读反馈
def getCallbackScore(useful_num, max_useful_num):
    if max_useful_num>0:
        return useful_num/max_useful_num
    else:
        return 0

#正态，u均值，d标准差
def getNormalScore(x, u =0, d=1 ):
    f = (1/ (math.sqrt(2*math.pi)*d))*math.exp(-(x-u)*(x-u)/(2*d*d))
    return f

#评论长度
def getLenScore(len, comment):
    na = 0
    nb=0
    words = comment.split(' ')
    for word in words:
        if word in owords:
            na += 1
        for level in levelwords:
            if word in level:
                nb += 1
    
    if (na + nb) <= 0 or len <=1:
        return 0
    ret = math.log(na + nb)/math.log(len)

    return ret
        

#图片数量
def getPicScore(pic_num, max_pic_num):
    if pic_num <= 0:
        pic_num = 1
    if pic_num > 9:
        pic_num = 9
    return pic_num/9


#程度级别
def getLevelScore(comment):
    keyword = ['啊', '呢', '唉']
    symbol = ['!', '?']
    ret = 0
    
    for word in comment:
        if word in keyword:
            ret += 0.7
        if word in symbol:
            ret +=0.3
    return ret
        
#情感词
def getFeelScore(comment):
    max_score = 50
    score = 0
    words = comment.split(' ')
    n = dict()
    n[0]=1
    n[1]=1
    n[2]=1
    n[3]=1
    for word in words:
        if word in feelwords:
            score += 1

        if word in levelwords[0]:
            n[0]+=1
        elif word in levelwords[1]:
            n[1]+=1
        elif word in levelwords[2]:
            n[2]+=1
        elif word in levelwords[3]:
            n[3]+=1
    score = 0.1 * n[0] + 0.2 * n[1] + 0.3 * n[2] + 0.4 * n[3]            
    return score 


def getOScore(comment):
    max_score = 30
    score = 0
    words = comment.split(' ')
    for word in words:
        if word in owords:
            score += 0.2
            
    if score > max_score:
        score = max_score
    return score / max_score


def statistic(raw_data_file_name, file_path):
    itemid = "result"
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)

    try:
        f_raw_data = open(file_path + '/'+raw_data_file_name, 'r', encoding='GBK')
    except Exception as err:
        print(err)
        return

    comments = list()
    for line in f_raw_data:
        line = line.rstrip()
        raw_data_json = eval(line)
        comments.append(raw_data_json)#['comments']
    f_raw_data.close()

    #只取x条
    # x = 50
    # comments = comments[:x]

    #取最早时间、最大图片数
    most_early_comment_date = 999999999999999
    max_pic_num = 0
    max_useful_num = 0
    max_timeliness = 0
    max_len_score = 0
    max_pic_score = 0
    max_oscore = 0
    max_level_score = 0
    max_feel_score = 0

    for each in comments:
        date = each['date'].replace(
            '年', '-').replace('月', '-').replace('日', '')
        date = date[:10]
        if len(date) != 0:
            timestamp = time.mktime(time.strptime(date, '%Y-%m-%d'))
            if most_early_comment_date > timestamp:
                most_early_comment_date = timestamp
            if max_timeliness < getTimelinessScore(timestamp, 0):
                max_timeliness = getTimelinessScore(timestamp, 0)

        content = each['content']
        content_split = ' '.join(jieba.cut(content))
        pic_num = len(each['photos'])
        if pic_num > max_pic_num:
            max_pic_num = pic_num

        useful=each['useful']
        if useful > max_useful_num:
            max_useful_num = useful
        
        if max_len_score < getLenScore(len(content), content_split):
            max_len_score = getLenScore(len(content), content_split)

        if max_oscore < getOScore(content_split):
            max_oscore = getOScore(content_split)

        if max_level_score < getLevelScore(content):
            max_level_score = getLevelScore(content)

        if max_feel_score < getFeelScore(content_split):
            max_feel_score = getFeelScore(content_split)

    #对所有评论进行计算分数
    comment_score_list = list()
    every_score_list=list()
    index = 1
    max_score = 0
    for each in comments:
        user_name = each['user']['nick']
        user_viplevel = each['user']['vipLevel']
        user_rank = each['user']['rank']
        content = each['content'].strip()
        content_split = ' '.join(jieba.cut(content))
        # if ('此用户没有填写评价' not in content) and len(content)<256:
        #     f_content.write(content+'。')
        #f_content.write(content+'\n')
        timestamp = 0
        date = each['date'].replace(
            '年', '-').replace('月', '-').replace('日', '')
        date = date[:10]
        if len(date) != 0:
            timestamp = time.mktime(time.strptime(date, '%Y-%m-%d'))
        else:
            timestamp = 0
        pic_num = len(each['photos'])
        useful = each['useful']

        score_list = list()
        #weight_list = [0.188775, 0.111426, 0.040004,0.108374,0.133871,0.208775, 0.208775]
        score_list.append(getCallbackScore(useful, max_useful_num))
        score_list.append(getTimelinessScore(timestamp, most_early_comment_date)/ max_timeliness)
        score_list.append(getLenScore(len(content), content_split)/ max_len_score)
        score_list.append(getPicScore(pic_num, max_pic_num)/ max_pic_num)
        score_list.append(getOScore(content_split)/ max_oscore)
        score_list.append(getLevelScore(content)/ max_level_score)
        score_list.append(getFeelScore(content_split) / max_feel_score)
        every_score_list.append(score_list)

        total_score =0
        score_str = ''
        for i in range(0, len(score_list)):
            score = score_list [i]
            score_str += str(decimal.Decimal(score).quantize(decimal.Decimal('0.000'))) + ','
            total_score += (score * weight_list[i])

        if max_score < total_score:
            max_score = total_score

        if '此用户没有填写评价' in content or '系统默认好评' in content:
            total_score = 0

        content = content.replace(',' , "，")
        comment_score_list.append((content, score_str, total_score, index))
        
        index += 1

    max_page = len(comment_score_list) / 100
    # max_page = 1
    for i in range(0, int(max_page)):
        print("page:" + str(i+1))
        total_list = list()
        total_score_list=list()
        #对前100条评论进行排序
        comment_score_list_100 = comment_score_list[i*100: i*100+100]
        orig_comment_score_list_100 = comment_score_list_100
        score_list_100 = every_score_list[i*100: i*100+100]

        #Cij
        for score_list in score_list_100:
            for n in range(0, len(score_list)):
                score_list[n] = score_list[n] * weight_list[n]

        #C+,C-
        Ca_list = list()
        Cs_list = list()
        for n in range(0, len(score_list_100[0])):
            Ca_list.append(0)
            Cs_list.append(999999999)
        for score_list in score_list_100:
            for n in range(0, len(score_list)):
                if score_list[n] > Ca_list[n]:
                    Ca_list[n] = score_list[n]
                if score_list[n] < Cs_list[n]:
                    Cs_list[n] = score_list[n]

        #正负理想解距离
        Sa_list = list()
        Ss_list = list()
        for score_list in score_list_100:
            suma = 0
            sums = 0
            for n in range(0, len(score_list)):
                suma += pow(score_list[n]-Ca_list[n], 2)
                sums += pow(score_list[n] - Cs_list[n], 2)
            Sa_list.append(math.sqrt(suma))
            Ss_list.append(math.sqrt(sums))

        for n in range(0, len(Sa_list)):
            total_score_list.append((Ss_list[n] / (Ss_list[n] + Sa_list[n]), n))

        sort_total_list = list(total_score_list)
        sort_total_list.sort(key = lambda score:score[0], reverse=True)

        #(content, score_str, total_score,index,,score_list)
        # for item in orig_comment_score_list_100:
        for item in total_score_list:
            total_score = str(decimal.Decimal(item[0]).quantize(decimal.Decimal('0.000')))
            #默认标号，文本，指标，量化总值
            total_list.append(str(item[1]+1) +',' + str(orig_comment_score_list_100[item[1]][0]) +',' + str(orig_comment_score_list_100[item[1]][1]) +total_score)

        #(content, score_str, total_score,index,score_list)
        tmp_list = list()
        # comment_score_list_100.sort(key=lambda comment_score: comment_score[2], reverse=True)#按总分降序
        index = 1
        for item in sort_total_list:
            total_score = str(decimal.Decimal(item[0]).quantize(decimal.Decimal('0.000')))
            # comment_score_list_100[item[1]] = (comment_score_list_100[item[1]], index)
            sort_total_list[index-1] = (sort_total_list[index - 1], index)
            tmp_list.append("," + str(index)  + ','+str(item[1]+1) + ',' + total_score + ','+comment_score_list_100[item[1]][0]+'\n')
            index += 1
            
        #(content, score_str, total_score,index)
        # comment_score_list_100.sort(key=lambda comment_score: comment_score[0][3], reverse=False)
        sort_total_list.sort(key=lambda index:index[0][1], reverse=False)
        index = 1
        # for item in comment_score_list_100:
        for item in sort_total_list:
            sorted_index = item[1]
            default_index = index
            total_score = str(decimal.Decimal(item[0][0]).quantize(decimal.Decimal('0.000')))
            #默认排序，本文排序，量化值
            total_list[index-1] += ("," + str(default_index) +"," + str(sorted_index)  +','+ total_score)
            total_list[index-1] += tmp_list[index - 1]
            # total_list[index-1] += item[0]
            index += 1

        f_total = open(file_path + itemid + '/total'+itemid+"_" + str(i)+".csv", 'w+', encoding='GBK')
        f_total.close()
        f_total = open(file_path + itemid + '/total'+itemid+"_"+ str(i)+".csv", 'a+', encoding='GBK')
        f_total.write(",,评论有用性量化特征\n")
        f_total.write(",,有用性指标,时效性指标,评论长度指标,图片数量指标评,属性词,语气强度,情感词,\n")
        f_total.write("默认标号,评论文本内容,T1,T2,T3,T4,T5,T6,T7,量化总值,默认排序,本文排序,量化值,本文排序,默认排序,量化值\n")
        for item in total_list:
            f_total.write(item)
        f_total.close()


if __name__ == '__main__':
    itemid_list = config.itemid_list
    file_path = config.file_path
    # for itemid in itemid_list:
    statistic("set_phone.txt", file_path)
