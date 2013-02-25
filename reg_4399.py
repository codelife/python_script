#!/usr/bin/python 
#-*-coding:utf-8-*-   
import httplib,urllib,urllib2,sys,cookielib;  #加载模块   
import time,re;
import traceback; 
import random
#定义需要进行发送的数据   
def main():
    qq_num=random.randrange(0, 55502034233)
    email=str(qq_num)+"@qq.com"
    params = urllib.urlencode({'postLoginHandler':'default','displayMode':'embed','appId':'www_home','manualReg':'false','regIdcard':'false','noEmail':'false','mainDivId':'embed_login_div','showRegInfo':'true','password':'123456','passwordveri':'123456','email':email ,'reg_eula_agree':'on'})
    #定义一些文件头   
    headers = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",   
               "User_Agent":"Mozilla/5.0 (Windows NT 6.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2",
               "Connection":"Keep-Alive","Referer":"http://ptlogin.4399.com/ptlogin/regFrame.do?postLoginHandler=default&redirectUrl=&displayMode=embed&css=&appId=www_home&noEmail=false&gameId=&regIdcard=false"};   
    #与网站构建一个连接   
    reg_url='http://ptlogin.4399.com/ptlogin/autoRegister.do'
    #vote_url='http://huodong.4399.com/2012/topgame/vote.php?id=360&t=0.2581907153837192'
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    result=opener.open(reg_url,params)
    result_str=result.read()
    try:
        file_id=time.strftime("%Y-%m-%d", time.localtime())
        fd_id=open('/tmp/'+str(file_id),'a')
        p=re.search('.*4399用户名.*?>(\d+).*',result_str)
        print p.group(1)
        fd_id.write(str(p.group(1))+'\n')
    except:
        print "reg fail"
    finally:
        fd_id.close()
    #vote_result=opener.open(vote_url)
    return 0
if __name__=="__main__":
    main()
    sys.exit(0)
    while True:
        try:
            count=10 #暂停的时间最大值(实际暂停时间为1-count之间的数)
            sleep_time=random.randrange(1,count)
            main()
            print 'sleeping .....%d' %sleep_time
            time.sleep(sleep_time)
        except:
            continue
