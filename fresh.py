#!/usr/local/bin/python
#-*-coding:utf-8-*-
import httplib,urllib, sys, time
import simplejson as json
#定义需要进行发送的数据
headers = {"Content-Type":"application/x-www-form-urlencoded","Connection":"Keep-Alive"};  
task=json.dumps({'urls':('http://www.domain.com/cur.js','http://www.domain.com','http://www.domain.com/index.html','http://www.domain.com/Client.swf')})
params = urllib.urlencode({'username' : 'name','password':'name1111','task':task})
conn = httplib.HTTPSConnection("r.chinacache.com");   
conn.request(method="POST",url="/content/refresh",body=params,headers=headers)   
print "已提交刷新请求,耐心等待........"
response = conn.getresponse();   
return_code=response.read()
#判断是否提交成功   
if response.status == 200:   
    print "发布成功!";   
    print '--------------------------------'
    #查询刷新进度
    code=return_code.split(':')[1].strip('}')
    print "query id is:%s" % code
    #conn_id = httplib.HTTPSConnection("r.chinacache.com");   
    #params_id = urllib.urlencode({'username':'name','password':'name1111','r_id':code})
    #conn_id.request(method="GET",url="/content/refresh/"+str(code) ,body=params_id,headers=headers)   
    #response_id = conn_id.getresponse();   
    #if response_id.status == 200:
    #    print "查询刷新结果成功"
    #    print response_id.read()
    #    print '--------------------------------'
    #    #TODO fresh progress
    #else:
    #    print "查询刷新结果失败"
else:   
    print "发布失败,请再次尝试．或者手动刷新";   
    print response.status
#关闭连接   
conn.close();
#返回处理后的数据   
print response.read()
