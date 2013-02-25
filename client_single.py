#!/usr/bin/env python
#coding=utf-8
#运行条件:
    #目录及命名规则:
    #1.线上项目目录:/usr/local/kor/client/ 
    #2.ssh用户需有sudo权限
    #3.本地客户端目录下的client目录
import subprocess
from fabric.api import run, env,sudo 
from fabric.operations import put,local
from fabric.context_managers import *
import time
import os
import sys
global server_dest_path
global server_src_path
global singal_file_dir
global dest_path
global local_path
client_dest_dir = "/usr/local/kor/" #游戏客户端所在目录,客户端目录client所在目录
client_src_dir = "/root/version/"   #内网游戏客户端目录,客户端目录client所在目录
singal_file_dir = "/root/version/singal_file/" #需要更新的文件放置在此目录
local_path = client_src_dir + "client/"
dest_path = client_dest_dir + "client/"
def add_version():
    with hide('stdout', 'stderr','running'):
        cur_value = sudo("awk -F'=' '/^var client_v/{print $2}' %s/cur.js | tr -d ';'" %dest_path)
        new_cur_value= int(cur_value) + 1
    date=time.strftime("%m.%d.%H.%M.%S")
    sudo("cp %s/cur.js %s/version_backup/cur.js.%s" %(dest_path,client_dest_dir,date))
    with hide('stdout', 'stderr','running'):
        sudo("sed -i '/^var client_v/s/%s/%s/' %s/cur.js" %(cur_value,new_cur_value,dest_path))
    print "\033[1;40;33mUpdate file cur.js successful\033[0m"
    print "\033[1;40;35mCurrent version is : %s\033[0m" % new_cur_value

def upload_singal_file(filename=""):
    date=time.strftime("%m.%d.%H.%M.%S")
    with hide('stdout', 'stderr','running'):
        file_value = sudo("awk -F'|' '/\<%s\>/{print $1}' %s/revision.swf " %(filename,dest_path))
        if file_value.isdigit():
            new_file_value = int(file_value) + 1 
        elif len(file_value)==0:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print "\033[1;40;31mcan't find the file %s\033[0m" %filename
            print "\033[1;40;31mupdate file %s manually\033[0m" %filename
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            return 1
        else:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            print "\033[1;40;31mfind more than one file %s in revision.swf\033[0m" %filename
            print "\033[1;40;31mupdate file %s manually\033[0m"  %filename
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            return 1
    with hide('stdout', 'stderr','running'):
        sudo("chmod -R 777 %s" %client_dest_dir)
    filename_path=sudo("find %s -name %s" %(dest_path,filename))
    if filename_path.count('\n'):
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print "\033[1;40;31mFind more than one file %s in %s\033[0m" %(filename,dest_path)
        print "\033[1;40;31mupdate file %s manually\033[0m"  %filename
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        return 1
    sudo("cp %s %s/version_backup/%s.%s" %(filename_path,client_dest_dir,filename,date))
    sudo("cp %s/revision.swf %s/version_backup/revision.swf.%s" %(dest_path,client_dest_dir,date))
    sudo("rm -f %s" %filename_path)
    put("%s/%s" %(singal_file_dir,filename),os.path.dirname(filename_path))
    local("rm %s/%s" %(singal_file_dir,filename))
    with hide('stdout', 'stderr','running'):
        output=sudo("sed -i 's/%s\(.*%s.*\)/%s\\1/' %s/revision.swf" %(file_value,filename,new_file_value,dest_path))
    print "\033[1;40;33mUpdate file revision.swf successful\033[0m"
    
def upload_client(host="",server_name="" ):
    '''upload file 
    '''

    with hide('stdout', 'stderr'):
        exist_client=sudo("if test -e %s ;then echo True;else echo False;fi" %dest_path )
        exist_bakdir=sudo("if test -e %s/version_backup ;then echo True;else echo False;fi" %client_dest_dir )

    if os.path.exists(local_path):
        with hide('stdout', 'stderr'):
            with lcd(client_src_dir):
                print "entering dir %s" %client_src_dir
                local("tar czvf new_client.tar.gz client",capture=False)
                put("new_client.tar.gz" , client_dest_dir)
    else:
        print "\033[1;40;31mdirectory %s is not exist in %s\033[0m" %(local_path,env.host_string)
        sys.exit(1)

    if exist_bakdir=="True":
        pass
    else:
        sudo("mkdir %s/version_backup" %client_dest_dir)

    if exist_client=="True":
        with hide('stdout', 'stderr'):
            with cd(client_dest_dir):
                print "entering dir %s" %client_dest_dir
                date=time.strftime("%m.%d.%H.%M.%S")
                sudo("mv client version_backup/client.%s" %date)
                sudo("tar xzvf new_client.tar.gz")
    else:
        print "\033[1;40;31mnot exists client in directory %s\033[0m" %client_dest_dir
        with hide('stdout', 'stderr'):
            with cd(client_dest_dir):
                sudo("tar xzvf new_client.tar.gz")
        
if __name__ == '__main__':
    #客户端列表
    client=["192.168.1.10:22"]
    for client_host in client:
        env.host_string = client_host 
        env.user = "username"
        env.password = "pass"
        for filename in os.listdir(singal_file_dir):
            print filename
        print "These files in %s will be update to %s" %(singal_file_dir,env.host_string)
        confirm=raw_input("Are you sure:(Y/N)")
        if confirm == "Y":
            for filename in os.listdir(singal_file_dir):
                upload_singal_file(filename)
            add_version()
        else:
            sys.exit(1)
