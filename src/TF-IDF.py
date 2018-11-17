import config
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

itemid = config.itemid
file_path = config.file_path

# itemid_list = [itemid]  # 手动加

if __name__ == '__main__':
    corpus = list()

    file_list = os.listdir(file_path)
    for itemid in file_list:
        try:
            f = open(file_path + itemid + '/jieba.txt', 'r+', encoding='UTF-8')
            corpus.append(f.read())
            f.close()
        except IOError:
            print("File is not accessible.")

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

    wordmap = dict()
    # for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    #     result = list()
    #     for j in range(len(word)):
    #         result.append((str(word[j]), float(weight[i][j])))

    for j in range(len(word)):
        for i in range(len(weight)):
            if word[j] in wordmap:
                wordmap[word[j]] += weight[i][j]
            else:
                wordmap[word[j]] = weight[i][j]

    result = list(wordmap.items())

    result.sort(
        key=lambda sortresult: sortresult[1], reverse=True)

    f = open(file_path + 'output.txt', 'w+', encoding='UTF-8')
    for item in result:
        f.write(item[0] + '\t' + str(item[1]) + '\n')
    f.close()
