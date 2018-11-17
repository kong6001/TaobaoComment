import config
import jieba
import jieba.posseg as pseg
import os

itemid = config.itemid
file_path = config.file_path

if __name__ == '__main__':
    file_list = os.listdir(file_path)
    for file in file_list:
        try:
            f = open(file_path + file + '/' +
                     'content.txt', 'r+', encoding='UTF-8')
            content = f.read()
            f.close()
        except:
            print("error")

        f = open(file_path + file + '/' + 'jieba.txt', 'w+', encoding='UTF-8')
        f.write(' '.join(jieba.cut(content)))
        f.close()
