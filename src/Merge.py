#将多家店铺的评论合入同一个文件
import json
import os
import config


file_path = config.file_path


def merge(itemid, com_list):
    if not os.path.exists(file_path + itemid):
        os.makedirs(file_path + itemid)

    try:
        f_raw_data = open(file_path + itemid +
                          '/raw_data.txt', 'r', encoding='GBK')
    except Exception as err:
        print(err)
        return

    for line in f_raw_data:
        raw_data_json = json.loads(line)
        com_list += raw_data_json['comments']
    f_raw_data.close()


item_list = config.itemid_list
com_list = list()
for item_id in item_list:
    merge(item_id, com_list)

f = open(file_path+"/set.txt", "w", encoding="GBK")
for com in com_list:
    f.write(str(com) + "\n")
f.close()
