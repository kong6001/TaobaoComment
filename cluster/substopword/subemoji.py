# -*- coding: utf-8 -*-
import re
import sys
import os

if len(sys.argv) > 2:
    print('input param error!')
    os._exit(0)

sys.argv.append('result.txt')
f = open(sys.argv[1], 'r+', encoding='UTF-8')
sss = f.read()
f.close()

try:
    # Wide UCS-4 build
    myre = re.compile(u'['
                      u'\U0001F300-\U0001F64F'
                      u'\U0001F680-\U0001F6FF'
                      u'\u2600-\u2B55]+',
                      re.UNICODE)
except re.error:
    # Narrow UCS-2 build
    myre = re.compile(u'('
                      u'\ud83c[\udf00-\udfff]|'
                      u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                      u'[\u2600-\u2B55])+',
                      re.UNICODE)

sss = myre.sub('。', sss)
print('OK')

f = open(sys.argv[1], 'w+', encoding='UTF-8')
f.write(sss)
f.close()
