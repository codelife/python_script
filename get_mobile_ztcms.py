#!/usr/local/bin/python3
import re
import os
import json
import time
day = time.strftime("%Y-%m-%d", time.localtime())
# 读取源文件
src_file = '/Users/lijunya/Downloads/30332.txt'
# 写入文件
dst_file = '/Users/lijunya/' + day + '.txt'
fd = open(src_file, 'r')
content = fd.readline()
content = re.sub('common_msg_.*\(', '', content)
content = content.replace(');', '')
content = json.loads(content)
content = content['RESULT']
dst_fd = open(dst_file, 'w')
for info in content:
    print(info[0], info[1], info[3])
    dst_fd.write(info[0] + '  ' + info[1] + '   ' + info[3])
    dst_fd.write("\r\n")
dst_fd.close()
