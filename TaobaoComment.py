# coding=utf-8

from __future__ import unicode_literals  # 解决json.dumps的中文乱码问题
import json
import os
import re  # 正则
import time
from urllib import request

# itemid = '540622763937'  # 184
# itemid = '547752478009'  # 1922
itemid = '545828211529'  # 10567,只能爬到5000条,原因不明

file_path = 'D:/taobao_comments/'

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


def getKeywordNumofComment(comment, dic_key_word):
    n = 0
    for item in dic_key_word:
        n += comment.count(item)
    return n


def getH1(exp):
    if exp > 0 and exp <= 3:
        return 0
    elif exp > 3 and exp <= 10:
        return 0.316
    elif exp > 10 and exp <= 40:
        return 0.447
    elif exp > 40 and exp <= 90:
        return 0.548
    elif exp > 90 and exp <= 150:
        return 0.632
    elif exp > 150 and exp <= 250:
        return 0.707
    elif exp > 251 and exp <= 500:
        return 0.775
    elif exp > 501 and exp <= 1000:
        return 0.837
    elif exp > 1001 and exp <= 2000:
        return 0.894
    elif exp > 2001 and exp <= 5000:
        return 0.949
    elif exp > 5000:
        return 1
    else:
        return 0


def getTotalUsefulNum(raw_data_list):
    useful = 0
    for item in raw_data_list:
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


def getH3(comment_timestamp, t_gap=30, param=1):
    t1 = time.time()
    t2 = comment_timestamp
    t_delta = int((t1 - t2)/(24*60*60))
    if t_delta < 30:
        t_delta = 30
    elif t_delta > 360:
        t_delta = 360

    return (t_gap * param) / t_delta


def getH4(comment_len):
    if comment_len <= 10:
        return 0.4
    elif comment_len > 10 and comment_len <= 30:
        return 0.6
    elif comment_len > 30 and comment_len <= 40:
        return 0.8
    elif comment_len > 40 and comment_len <= 50:
        return 0.9
    elif comment_len > 50 and comment_len <= 80:
        return 1
    elif comment_len > 80 and comment_len <= 90:
        return 0.95
    elif comment_len > 90 and comment_len <= 110:
        return 0.9
    elif comment_len > 110 and comment_len <= 150:
        return 0.7
    elif comment_len > 150 and comment_len <= 200:
        return 0.5
    else:
        return 0.3


def getH5(pic_num):
    if pic_num <= 0:
        return 0.5
    elif pic_num > 0 and pic_num <= 2:
        return 0.8
    elif pic_num > 2 and pic_num <= 3:
        return 1
    elif pic_num > 3 and pic_num <= 6:
        return 0.8
    elif pic_num > 6:
        return 0.7


def getKofD1(comment, v=[0.15, 0.25, 0.2, 0.15, 0.25]):
    dics = [dic_l1, dic_l2, dic_l3, dic_l4, dic_l5]
    n = []
    for dic in dics:
        n.append(getKeywordNumofComment(comment, dic))

    k = 0
    for i in range(len(n)):
        k += (v[i] * n[i])

    return k


def getMaxKofD1(raw_data_list):
    k_list = []
    for item in raw_data_list:
        content = item['content']
        k_list.append(getKofD1(content))

    return max(k_list)


def getD1(comment, k_max):
    return getKofD1(comment) / k_max


def getAofD2(comment, param1=0.65, param2=0.35):
    state_word = ['啊', '哇', '哎', '唉', '呀', '哈']
    punctuation = ['？', '！', '……']
    n1 = getKeywordNumofComment(comment, state_word)
    n2 = getKeywordNumofComment(comment, punctuation)

    return param1 * n1 + param2 * n2


def getMaxAofD2(raw_data_list):
    A_list = []
    for item in raw_data_list:
        A_list.append(getAofD2(item['content']))

    return max(A_list)


def getBofD2(comment, v=[0.15, 0.25, 0.3, 0.5]):
    dic_l1 = ['稍', '多少', '有点', '有些', '略微', '稍微']
    dic_l2 = ['很', '比较', '较为', '不太', '不打', '不很', '不甚']
    dic_l3 = ['太', '挺', '满', '越', '更', '好', '大', '特别',
              '甚至', '更加', '尤其', '越发', '十分', '非常', '格外']
    dic_l4 = ['最', '极', '顶', '无比', '最为', '极其', '万分']
    dics = [dic_l1, dic_l2, dic_l3, dic_l4]
    n = []
    for dic in dics:
        n.append(getKeywordNumofComment(comment, dic))

    B = 0
    for i in range(len(n)):
        B += (v[i] * n[i])
    return B


def getMaxBofD2(raw_data_list):
    B_list = []
    for item in raw_data_list:
        B_list.append(getBofD2(item['content']))

    return max(B_list)


def getD2(comment, A_max, B_max):
    A_part = getAofD2(comment) / A_max
    B_part = getBofD2(comment)/B_max
    return (A_part+B_part)/2


def getD3(comment, append, gamma=3, fai=10):
    W0 = len(comment)
    Wadd = 0
    if any(append):
        Wadd = len(append['content'])
    if 0 == Wadd:
        return 0

    ratio = W0/Wadd

    Nadd = 0
    dics = [dic_l1, dic_l2, dic_l3, dic_l4]
    for dic in dics:
        Nadd += getKeywordNumofComment(append['content'], dic)

    if 0 == Nadd:
        return 0

    if ratio > gamma or ratio < (1 / gamma):
        return 1
    else:
        if Nadd > fai:
            return 1
        else:
            return Nadd/fai


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
            raw_data += response_json['comments']

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

    f = open(file_path + itemid + '/' +
             'raw_data.json', 'a+', encoding='UTF-8')
    raw_data_json = json.dumps(raw_data, ensure_ascii=False)
    f.write(raw_data_json)
    f.close()


def main():
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)

    f_output = open(file_path + itemid + '/output.txt', 'w', encoding='UTF-8')
    f_result = open(file_path + itemid + '/result.txt', 'w', encoding='UTF-8')
    f_result_review = open(file_path + itemid +
                           '/result_for_review.txt', 'w', encoding='UTF-8')
    f_result_top = open(file_path + itemid +
                        '/result_top.txt', 'w', encoding='UTF-8')

    raw_data_list = []
    result_list = []

    getRawData(file_path, raw_data_list)
    # raw_data_list = json.loads(
    #    open(file_path+itemid+'/raw_data.json', 'r', encoding='UTF-8').read())

    k_max = getMaxKofD1(raw_data_list)
    a_max = getMaxAofD2(raw_data_list)
    b_max = getMaxBofD2(raw_data_list)
    useful_total_num = getTotalUsefulNum(raw_data_list)

    # f_output.write('共{}条评论\n'.format(len(raw_data_list)))
    index = 1
    for each in raw_data_list:
        user_name = each['user']['nick']
        user_viplevel = each['user']['vipLevel']
        user_rank = each['user']['rank']
        content = each['content']
        date = each['date'].replace(
            '年', '-').replace('月', '-').replace('日', '')
        timestamp = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M'))
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
            append_time = append_comment['dayAfterConfirm']
            append_pic_num = len(append_comment['photos'])
            f_output.write('追评：'+append_content+'\t')
            f_output.write('追评时间：'+str(append_time)+' 天后'+'\t')
            f_output.write('追评图片数：' + str(append_pic_num) + '\t')

        H1 = getH1(user_rank)
        H2 = getH2(useful, useful_total_num)
        H3 = getH3(timestamp)
        H4 = getH4(len(content))
        H5 = getH5(pic_num)
        D1 = getD1(content, k_max)
        D2 = getD2(content, a_max, b_max)
        D3 = getD3(content, append_comment)

        M1 = 0.2 * (H1 + H2 + H3 + H4 + H5)
        M2 = 0.3 * D1 + 0.5 * D2 + 0.2 * D3

        result = M1+0.5*M2
        result_tuple = (result, index)
        result_list.append(result_tuple)

        f_output.write('H1:'+str(H1)+'\t')
        f_output.write('H2:'+str(H2)+'\t')
        f_output.write('H3:'+str(H3)+'\t')
        f_output.write('H4:'+str(H4)+'\t')
        f_output.write('H5:'+str(H5)+'\t')
        f_output.write('D1:'+str(D1)+'\t')
        f_output.write('D2:'+str(D2)+'\t')
        f_output.write('D3:' + str(D3) + '\t')
        f_output.write('M1:{}'.format(M1) + '\t')
        f_output.write('M2:{}'.format(M2)+'\t')
        f_output.write('result:{}'.format(result)+'\t')
        f_output.write('\n')

        f_result.write(str(result)+'\n')
        f_result_review.write(str(round(M1, 2)) + " " +
                              str(round(M2, 2)) + "\n")
        index += 1

    result_list = sorted(result_list, reverse=True)
    for result_tuple in result_list:
        f_result_top.write(str(result_tuple) + '\n')

    f_result_top.close()
    f_output.close()
    f_result.close()


main()
