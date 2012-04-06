#!/usr/bin/python   
#-*-coding:utf-8-*-   
 
import urllib,urllib2,sys;  #加载模块   
import random
#定义需要进行发送的数据   
def main():
    randnum=random.randint(1,32423423234)
    params_seegame = urllib.urlencode({'':randnum,'username':'16156240','password'
        :'ff81e29ca22d9d897ee18a62a443b9c6'});   
    opener = urllib2.build_opener()
    ret_seegame=opener.open("http://domainname.com/login/baidulogin",
            params_seegame)
    data =ret_seegame.read()
    code=data.split(',')[-2].split(":")[1].strip('}').strip('"')
    cert=data.split(',')[-1].split(":")[1].strip('}').strip('"')
    if code=="0":
        pass
    else:
        return 1
    #baidu 阶段的验证,10X的错误都跟这个阶段有关系
    opener_baidu = urllib2.build_opener()
    params_baidu=urllib.urlencode({'id':'16156240','cert':cert});   
    ret_baidu=opener_baidu.open("http://domainname.com/tp/kukuAuth.jsp",
            params_baidu)
    baidu_code=ret_baidu.read().split(',')[-2].split(":")[1].strip('}').strip('"')
    if baidu_code=="0":
        pass
    else:
        return 2
    return 0
    #判断是否提交成功   
if __name__=="__main__":
   try:
       ret =  main()
   except:
       print 3
       sys.exit(1)
   print ret
