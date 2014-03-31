#!/usr/bin/python
#-*-coding:utf-8-*-

import httplib
import urllib
import sys
# 加载模块
import traceback
# 定义需要进行发送的数据


def main():
    params = urllib.urlencode(
        {'password': 'ff81e29ca22d9d897ee18a62a443b9c6', 'username': '4443650'})
    # 定义一些文件头
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Connection": "Keep-Alive", "Referer": "http"}
    # 与网站构建一个连接
    conn = httplib.HTTPConnection("account.game.com")
    # 开始进行数据提交   同时也可以使用get进行
    conn.request(
        method="POST",
        url="/login/login?20051.266438339837",
        body=params,
        headers=headers)
    # 返回处理后的数据
    # conn.sock.settimeout(2.0)
    response = conn.getresponse()
    data = response.read()
    id = data.split(',')[0].split(":")[1].strip('"')
    code = data.split(',')[1].split(":")[1]
    # 判断是否提交成功
    if response.status == 200:
        if (code == "0" and id == "4443650"):
            print "0"
        else:
            print "1"
    else:
        print "1"
    conn.close()
if __name__ == "__main__":
    try:
        main()
    except:
        print "1"
