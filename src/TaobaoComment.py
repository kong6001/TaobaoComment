# coding=utf-8

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

itemid = config.itemid
file_path = config.file_path
len_avg = config.len_avg
len_variance = config.len_variance

levelwords = [config.level1words, config.level2words, config.level3words, config.level4words]
feelwords = []
file_list = os.listdir('feelwords')
for file in file_list:
    f = open('feelwords/' + file, 'r+', encoding='GBK')
    words = f.readlines()
    for word in words:
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

    if rank > 5000:
        score += 1
    elif rank <= 5000 and rank > 2000:
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
    max_score = 30
    score = 0
    words = comment.split(' ')
    for word in words:
        if word in owords:
            score += 1
        # if word in config.wo2:
        #     score += 1
        # if word in config.wo3:
        #     score += 1
            
    if score > max_score:
        score = max_score
    return score / max_score


def main():
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)


    # f_output = open(file_path + itemid + '/output.txt', 'w', encoding='UTF-8')
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


    comment_score_list = list()
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
        weight_list = [0.188775, 0.111426, 0.100004,0.088374,0.133871,0.188775, 0.188775]
        score_list.append(getCredibilityScore(user_name,user_rank))
        score_list.append(getTimelinessScore(timestamp, most_early_comment_date))
        score_list.append(getCallbackScore(useful, max_useful_num))
        score_list.append(getLenScore(len(content)))
        score_list.append(getPicScore(pic_num, max_pic_num))
        #score_list.append(getLevelScore(content_split))
        score_list.append(getFeelScore(content_split))
        score_list.append(getOScore(content_split))

        total_score =0
        score_str = ''
        for i in range(0, len(score_list)):
            score = score_list [i]
            score_str += str(decimal.Decimal(score).quantize(decimal.Decimal('0.000'))) + '\t'
            total_score += (score * weight_list[i])

        if '此用户没有填写评价' in content or '系统默认好评' in content:
            total_score = 0

        comment_score_list.append((content, score_str, total_score,index))
        index+=1

    f_scores.close()

    comment_score_list = comment_score_list[0:100]
    orig_comment_score_list = comment_score_list
    
    # first_comment_list = orig_comment_score_list[0:10]
    # second_comment_list = orig_comment_score_list[10:20]
    # third_comment_list = orig_comment_score_list[20:]

    # second_comment_list.sort(key=lambda a: a[2], reverse=True)
    # comment_score_list = list()
    # comment_score_list = first_comment_list + second_comment_list + third_comment_list
    
    f_origin_content = open(file_path + itemid + u'/按照默认排序的评论内容.txt', 'w', encoding='UTF-8')
    f_origin_score = open(file_path+itemid+'/按照默认排序的得分情况.txt', 'w', encoding='UTF-8')
    f_sorted_content = open(file_path+itemid+'/新排序的评论内容.txt', 'w', encoding='UTF-8')
    f_sorted_score = open(file_path+itemid+'/新排序的得分情况.txt', 'w', encoding='UTF-8')
    f_change = open(file_path+itemid+'/change.txt', 'w', encoding='UTF-8')
    f_change_noscore = open(file_path + itemid + '/change_noscore.txt', 'w', encoding='UTF-8')

    f_sorted_score.write('新名次\t可信度\t时效性\t有用性\t评论长度\t图片\t情感词\t属性词\t总分\t原名次\n')
    for item in orig_comment_score_list:
        total_score = str(decimal.Decimal(item[2]).quantize(decimal.Decimal('0.000')))
        f_origin_content.write(str(item[3]) +'\t' +total_score +'\t'+ str(item[0])+'\n')
        f_origin_score.write(str(item[1]) + '\t' + total_score + '\n')

    #(content, score_str, total_score,index)
    comment_score_list.sort(key=lambda comment_score: comment_score[2], reverse=True)
    index = 1
    for item in comment_score_list:
        total_score = str(decimal.Decimal(item[2]).quantize(decimal.Decimal('0.000')))
        f_sorted_content.write(str(item[3]) +'\t' +total_score +'\t'+str(item[0])+'\n')
        f_sorted_score.write(str(index)+'\t'+str(item[1]) + '\t' + total_score + '\t'+str(item[3])+ '\n')
        f_change.write(str(item[3]) + '\t' + str(index) + '\t' + total_score+'\n')
        f_change_noscore.write(str(item[3]) + '\t' + str(index) + '\n')
        
        comment_score_list[index-1] = (item, index)
        index += 1
        
    f_orgin_content2 = open(file_path + itemid + '/origin_content2.txt', 'w', encoding='UTF-8')
    f_orgin_score2 = open(file_path + itemid + '/按照默认排序的得分情况以及新排序名次.txt', 'w', encoding='UTF-8')

    f_orgin_score2.write('原名次\t可信度\t时效性\t有用性\t评论长度\t图片\t情感词\t属性词\t总分\t新名次\n')
    comment_score_list.sort(key=lambda comment_score: comment_score[0][3], reverse=False)
    for item in comment_score_list:
        sorted_index = item[1]
        item =  item[0]
        total_score = str(decimal.Decimal(item[2]).quantize(decimal.Decimal('0.000')))
        f_orgin_content2.write(str(sorted_index) +'\t' +total_score +'\t'+str(item[0])+'\n')
        f_orgin_score2.write(str(item[3]) + '\t' + str(item[1]) + '\t' + total_score +'\t'+str(sorted_index)+ '\n')
        index += 1


    f_sorted_content.close()

if __name__ == '__main__':
    main()
