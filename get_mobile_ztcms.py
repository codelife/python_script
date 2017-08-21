#!/usr/local/bin/python3
import re
import os
import json
import time
from datetime import datetime
type = 'csv'
if(type == 'csv'):
    sep = ","
else:
    sep = ' '
dayOfWeek = datetime.now().weekday()
if dayOfWeek == 0:
    # 星期天没有开户记录, 所以获取上周五的数据
    count = 3
else:
    count = 1
day = time.strftime("%m%d", time.localtime(time.time()-86400*count))
pre_day = time.strftime("%m%d", time.localtime(time.time()-86400*(count+1)))
# 读取源文件
src_file = '/Users/lijunya/Downloads/' + day + '.txt'
# 写入文件
dst_file = '/Users/lijunya/Downloads/' + day + '_format.' + type
pre_file = '/Users/lijunya/Downloads/' + pre_day + '_format.' + type
fd = open(src_file, 'r')
content = fd.readline()
content = re.sub('common_msg_.*\(', '', content)
content = content.replace(');', '')
content = json.loads(content)
content = content['RESULT']
dst_fd = open(dst_file, 'w')
for info in content:
    dst_fd.write(info[0] + sep + info[1] + sep + str(info[3]))
    dst_fd.write("\r\n")
dst_fd.close()
print('---------------Done-------------')
print(dst_file)
os.unlink(src_file)
os.unlink(pre_file)
