f = open('origin_content.txt', 'r', encoding='UTF-8')

lines = f.readlines()

li = []
for line in lines:
    l = line.strip().split('\t')
    li.append(l)

li.sort(key=lambda d: d[1], reverse=True)

f = open('sort.txt', 'w', encoding='UTF-8')
for l in li:
    st = str()
    for i in l:
        st += str(i)+'\t'
    f.write(st+'\n')
