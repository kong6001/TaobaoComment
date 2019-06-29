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
    return (time_stamp-most_early_timestamp) / (today_timestamp - most_early_timestamp)


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
def getLenScore(len):
    score = 0
    if len >= 50 and len < 70:
        score =  1
    elif len >= 70:
        score = (1-(len-70)/100)
    elif len < 50:
        score = (1 - (50 - len) / 50)

    if score < 0:
        score = 0
    return score
        

#图片数量
def getPicScore(pic_num, max_pic_num):
    if max_pic_num != 0:
        return pic_num / max_pic_num
    return 0


#程度级别
def getLevelScore(comment):
    max_score = 15
    score = 0
    words = comment.split(' ')
    for word in words:
        if word in levelwords[0]:
            score += 1
        elif word in levelwords[1]:
            score += 2
        elif word in levelwords[2]:
            score += 3
        elif word in levelwords[3]:
            score += 4
    
    if score > max_score:
        score = max_score
    return score / max_score
        
#情感词
def getFeelScore(comment):
    max_score = 50
    score = 0
    words = comment.split(' ')
    for word in words:
        if word in feelwords:
            score += 1

        if word in levelwords[0]:
            score += 0.5
        elif word in levelwords[1]:
            score += 1
        elif word in levelwords[2]:
            score += 1.5
        elif word in levelwords[3]:
            score += 2
            
    if score > max_score:
        score = max_score
    return score / max_score


def getOScore(comment):
    max_score = 15
    score = 0
    words = comment.split(' ')
    for word in words:
        if word in owords:
            score += 1
            
    if score > max_score:
        score = max_score
    return score / max_score


def statistic(raw_data_file_name, file_path):
    itemid = "result"
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)

    f_scores = open(file_path+itemid+'/scores.txt', 'w', encoding='GBK')
    try:
        f_raw_data = open(file_path + '/'+raw_data_file_name, 'r', encoding='GBK')
    except Exception as err:
        print(err)
        return

    comments = list()
    for line in f_raw_data:
        line = line.rstrip()
        raw_data_json = eval(line)
        comments.append(raw_data_json)
    f_raw_data.close()

    #只取x条
    # x = 50
    # comments = comments[:x]

    #取最早时间、最大图片数
    most_early_comment_date = 999999999999999
    max_pic_num = 0
    max_useful_num = 0

    for each in comments:
        date = each['date'].replace(
            '年', '-').replace('月', '-').replace('日', '')
        date = date[:10]
        if len(date) != 0:
            timestamp = time.mktime(time.strptime(date, '%Y-%m-%d'))
            if most_early_comment_date > timestamp:
                most_early_comment_date = timestamp

        content = each['content']
        pic_num = len(each['photos'])
        if pic_num > max_pic_num:
            max_pic_num = pic_num

        useful=each['useful']
        if useful > max_useful_num:
            max_useful_num = useful


    #对所有评论进行计算分数
    comment_score_list = list()
    index = 1
    max_score = 0
    for each in comments:
        user_name = each['user']['nick']
        user_viplevel = each['user']['vipLevel']
        user_rank = each['user']['rank']
        content = each['content'].strip()
        content_split = ' '.join(jieba.cut(content))
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
        weight_list = [0.10, 0.10, 0.00,0.30,0.30,0.10, 0.10]
        score_list.append(getCredibilityScore(user_name,user_rank))
        score_list.append(getTimelinessScore(timestamp, most_early_comment_date))
        score_list.append(getCallbackScore(useful, max_useful_num))
        score_list.append(getLenScore(len(content)))
        score_list.append(getPicScore(pic_num, max_pic_num))
        #score_list.append(getLevelScore(content_split))
        score_list.append(getOScore(content_split))
        score_list.append(getFeelScore(content_split))

        total_score =0
        score_str = ''
        for i in range(0, len(score_list)):
            score = score_list [i]
            score_str += str(decimal.Decimal(score).quantize(decimal.Decimal('0.000'))) + ','
            total_score += (score * weight_list[i])

        content = content.replace(',' , "，")
        comment_score_list.append((content, score_str, total_score,index))
        index+=1

    f_scores.close()

    max_page = len(comment_score_list) / 100
    for i in range(0, int(max_page)):
        print("page: "+ str(i))
        total_list = list()
        #对前100条评论进行排序
        comment_score_list_100 = comment_score_list[i*100: i*100+100]
        orig_comment_score_list_100 = comment_score_list_100
        
        f_origin_content = open(file_path + itemid + '/按照默认排序的评论内容.csv', 'w', encoding='GBK')
        f_origin_score = open(file_path+itemid+'/按照默认排序的得分情况.txt', 'w', encoding='GBK')
        f_sorted_content = open(file_path+itemid+'/新排序的评论内容.txt', 'w', encoding='GBK')
        f_sorted_score = open(file_path+itemid+'/新排序的得分情况.csv', 'w', encoding='GBK')

        #(content, score_str, total_score,index)
        for item in orig_comment_score_list_100:
            total_score = str(decimal.Decimal(item[2]).quantize(decimal.Decimal('0.000')))
            #默认标号，文本，指标，量化总值
            f_origin_content.write(str(item[3]) +',' + str(item[0]) +',' + str(item[1]) +total_score  +'\n')
            #f_origin_score.write(str(item[1]) + ',' + total_score + '\n')
            total_list.append(str((item[3]-1)%100 +1) +',' + str(item[0]) +',' + str(item[1]) +total_score)

        #(content, score_str, total_score,index)
        tmp_list = list()
        f_sorted_score.write('新名次,内容,可信度,时效性,有用性,评论长度,图片,属性词,情感词,总分,原名次\n')
        comment_score_list_100.sort(key=lambda comment_score: comment_score[2], reverse=True)#按总分降序
        index = 1
        for item in comment_score_list_100:
            total_score = str(decimal.Decimal(item[2]).quantize(decimal.Decimal('0.000')))
            #f_sorted_content.write(str(item[3]) +',' +total_score +','+str(item[0])+'\n')
            #本文排序，默认排序，量化值
            f_sorted_score.write(str(index)  + ','+str(item[3]) + ',' + total_score + '\n')
            
            comment_score_list_100[index-1] = (item, index)
            tmp_list.append("," + str(index)  + ','+str((item[3]-1)%100 +1) + ',' + total_score+ ','+item[0] + '\n')
            index += 1
            
        f_orgin_content2 = open(file_path + itemid + '/origin_content2.txt', 'w', encoding='GBK')
        f_orgin_score2 = open(file_path + itemid + '/按照默认排序的得分情况以及新排序名次.csv', 'w', encoding='GBK')

        #(content, score_str, total_score,index)
        f_orgin_score2.write('原名次,内容,可信度,时效性,有用性,评论长度,图片,属性词,情感词,总分,新名次\n')
        comment_score_list_100.sort(key=lambda comment_score: comment_score[0][3], reverse=False)
        index = 1
        for item in comment_score_list_100:
            sorted_index = item[1]
            item =  item[0]
            total_score = str(decimal.Decimal(item[2]).quantize(decimal.Decimal('0.000')))
            #默认排序，本文排序，量化值
            f_orgin_score2.write(str(index) +"," + str(sorted_index)  +','+ total_score + '\n')
            total_list[index-1] += ("," + str(index) +"," + str(sorted_index)  +','+ total_score)
            total_list[index-1] += tmp_list[index - 1]
            index += 1

        f_sorted_content.close()

        f_total = open(file_path + itemid + '/total'+itemid+"_" + str(i)+".csv", 'w+', encoding='GBK')
        f_total.close()
        f_total = open(file_path + itemid + '/total'+itemid+"_"+ str(i)+".csv", 'a+', encoding='GBK')
        f_total.write(",,评论有用性量化特征\n")
        f_total.write(",,评论者可信度指标,评论时效性指标,评论者反馈指标,评论长度指标,图片数量指标评,评论全面性指标,评论感染力指标,\n")
        f_total.write("默认标号,评论文本内容,T1,T2,T3,T4,T5,T6,T7,量化总值,默认排序,本文排序,量化值,本文排序,默认排序,量化值\n")
        for item in total_list:
            f_total.write(item)
        f_total.close()


if __name__ == '__main__':
    itemid_list = config.itemid_list
    file_path = config.file_path
    # for itemid in itemid_list:
    statistic("set_shoe.txt", file_path)
