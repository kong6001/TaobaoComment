import os

f = open('test.xml', 'r', encoding='UTF-8')
if not os.path.exists('output'):
    os.makedirs('output')

lines = f.readlines()
output = ['<?xml version="1.0" encoding="utf-8" ?>\n']
index = 0
begin = 0
for line in lines:
    if '<xml4nlp>' in line:
        begin = 1
    if begin == 1:
        output.append(line)

    if '</xml4nlp>' in line:
        f_o = open('output/'+str(index)+'.txt', 'w', encoding='UTF-8')
        f_o.writelines(output)
        f_o.close()
        output.clear()
        output.append('<?xml version="1.0" encoding="utf-8" ?>\n')
        begin = 0
        index += 1
