import config
import os
import os.path
import math

rootdir = config.file_path
lens = []
len_sum = 0
# 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
for parent, dirnames, filenames in os.walk(rootdir):
    for dirname in dirnames:  # 输出文件夹信息
        f = open(rootdir + dirname + '/' +
                 'content.txt', 'r+', encoding='UTF-8')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n').strip()
            lens.append(len(line))
            len_sum += len(line)


lens.sort()
M = len_sum/len(lens)
print('中位数:' + str(lens[int(len(lens) / 2)]))
print('平均数:' + str(M))

s = 0
for len_ in lens:
    s += (len_ - M) * (len_ - M)

s = s * s / len(lens)
print("方差:" + str(s))
print("标准差:" + str(math.sqrt(s)))


# 中位数:22
# 平均数:35.71935109060172
# 方差:592647021686.9303
# 标准差:769835.7108415602