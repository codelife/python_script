#!/usr/bin/python
import socket  
import re
import struct
import subprocess
import MySQLdb as mdb
import time
def query(start,stop):
    #dir server ip address
    remote_host = '192.168.1.123' 
    remote_port = 80
    len=29
    command_id=106
    unknow_id=49
    account=322580763
    null1=0
    query_str=struct.pack('>ibiiiiii',len,unknow_id,command_id,account,null1,start,stop,null1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((remote_host, remote_port))  
    sock.send(query_str)  
    result_file=open("result.txt",'a')
    sock.settimeout(2)
    try:
        response_data = sock.recv(4096)  
        result_file.write(repr(response_data))
        response_data = sock.recv(4096)  
        result_file.write(repr(response_data))
        response_data = sock.recv(4096)  
        result_file.write(repr(response_data))
    except:
        pass
    sock.close( ) 
    result_file.close()

def insert_online(database,table,count,base_dir_num):
    try:
        conn=mdb.connect('localhost','online','online_passwd',database,3306,'/tmp/mysql.sock')
        cur=conn.cursor()
        create_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        ret=cur.execute("insert into %s (online_num,create_time,base_dir_num) values (%d,'%s',%d)" %(table,count,create_time,base_dir_num))
        return ret
        conn.close()
    except:
        print "exception output............."
        return 1

start = 1
stop = 100
print "start querying ...."
while start<=3701:
    if start>=1000 and start<3501:
        start+=100
        stop+=100
        continue
    query(start,stop)
    start+=100
    stop+=100
online_num=open("result.txt",'r')
#print online_num.read()
p=re.findall(r'\\x0(\d)\d{1,3}\.',online_num.read())
base_dir_num = len(p)
count=0
for i in p :
    count+=int(i)
print count
subprocess.call("rm result.txt",shell=True)
insert_online("game_owner","game_name",count,base_dir_num)
