import sys

file_stopword = open('stopword.txt', 'r', encoding='UTF-8')
stopword = list()
for line in file_stopword:
    stopword.append(line.strip())
file_stopword.close()

sys.argv.append('result.txt')

f = open(sys.argv[1], 'r+', encoding='UTF-8')
lines = f.readlines()
f.close()

f = open(sys.argv[1], 'w+', encoding='UTF-8')

for line in lines:
    line = line.strip()
    words = line.split(' ')
    _words = []
    for i in range(0, len(words)):
        word = words[i]
        if word not in stopword:
            _words.append(word)

    line = ' '.join(_words)+'\n'

    f.write(line)

f.close()
