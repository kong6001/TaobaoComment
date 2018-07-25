from urllib import request
import json
import re


# def SpiderAttack():


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.37'
}

itemid = '39595400262'
# itemid = '546495252822'
# itemid = '573358934465'
file_path = 'D:/taobao_comments_'+itemid+'.txt'

f = open(file_path, 'a+')
for i in range(1, 11):
    try:
        url = ('https://rate.taobao.com/feedRateList.htm?auctionNumId=' +
               itemid + '&currentPageNum={}').format(str(i))
        res = request.Request(url, method='GET', headers=headers)
        byte = request.urlopen(res).read()
        string = byte.decode('UTF-8')

        #string = open('2.txt', 'r', encoding='UTF-8').read()
        string = re.sub('[\r\t\n]', '', string)
        string = string.strip(')')
        string = string.strip('(')
        ratelist = json.loads(string)['comments']

        for each in ratelist:
            user_name = each['user']['nick']
            user_viplevel = each['user']['vipLevel']
            user_rank = each['user']['rank']
            content = each['content']
            time = each['date']
            pic_num = len(each['photos'])
            useful = each['useful']
            f.write('用户名：' + user_name + '\t')
            f.write('VIP等级：' + str(user_viplevel) + '\t')
            f.write('用户等级：'+str(user_rank)+'\t')
            f.write('评论：'+content+'\t')
            f.write('时间：'+time+'\t')
            f.write('图片数：' + str(pic_num) + '\t')
            f.write('点赞数：' + str(useful) + '\t')

            append_comment = each['appendList']
            if any(append_comment):
                append_comment = append_comment[0]
                append_content = append_comment['content']
                append_time = append_comment['dayAfterConfirm']
                append_pic_num = len(append_comment['photos'])
                f.write('追评：'+append_content+'\t')
                f.write('追评时间：'+str(append_time)+' 天后'+'\t')
                f.write('追评图片数：' + str(append_pic_num) + '\t')

            f.write('\n')
    except:
        print('爬取第'+str(i)+'页出现问题')
        continue
f.close()
