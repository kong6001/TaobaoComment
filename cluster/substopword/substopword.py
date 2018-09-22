import sys

file_stopword = open('stopword.txt', 'r', encoding='UTF-8')
stopword = list()
for line in file_stopword:
    stopword.append(line)
file_stopword.close()

sys.argv.append('result.txt')

f = open(sys.argv[1], 'r+', encoding='UTF-8')
lines = f.readlines()
f.close()

f = open(sys.argv[1], 'w+', encoding='UTF-8')
for line in lines:
    if line not in stopword:
        f.write(line)
f.close()
