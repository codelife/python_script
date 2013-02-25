#!/usr/bin/python   
#-*-coding:utf-8-*-   
 
import httplib,urllib,sys;  #加载模块   
import traceback; 
#定义需要进行发送的数据   
def main():
    params = urllib.urlencode({'sPasswd':'8865441','sEmail':'kklijun4@qq.com','sRealName':'李俊','sIdNumber':'440106198101010155','sSex':'0','sYear':'2011','sMonth':'1','sDay':'1','sFlag':'','uid':'0'});   
    #定义一些文件头   
    headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",   
               "Connection":"Keep-Alive","Referer":"http://account.game.com/"};   
    #与网站构建一个连接   
    conn = httplib.HTTPConnection("account.game.com");   
    #conn = httplib.HTTPConnection("192.168.1.136",port="88");   
    #开始进行数据提交   同时也可以使用get进行   
    conn.request(method="POST",url="/register/active",body=params,headers=headers);   
    #返回处理后的数据   
    conn.sock.settimeout(2.0)
    response = conn.getresponse();   
    data =response.read()
    code=data.split(',')[0].split(":")[1]
    #判断是否提交成功   
    if response.status == 200:   
        if code=="-3":
            print 0;
        if code=="0":
            print 0;
    else:   
        print "";   
    conn.close()
if __name__=="__main__":
    try:
        main()
    except:
        print "1";
