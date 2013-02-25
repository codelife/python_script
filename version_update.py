#!/usr/bin/env python
#coding=utf-8
#运行条件:
    #目录及命名规则:
    #1.线上项目目录:/usr/local/kor/server/ --> 子服务(dir)目录-->/usr/local/kor/server/dir/-->子服务(dir)进程名-->DirServer
    #                                                                                      -->子服务(dir)so名称-->dir.so
    #2.ssh用户需有sudo权限
import subprocess
from fabric.api import run, env,sudo 
from fabric.operations import put,local
from fabric.context_managers import *
import time
import os
import sys
global server_dest_path
global server_src_path
server_dest_path="/usr/local/kor/server/" #线上游戏"项目"目录
server_src_path = "/home/devuser/programmer/server/server/" #内网游戏开发目录
xml_src_path = "/home/devuser/programmer/server/server/config/" ##内网配置xml文件目录
xml_dest_path= "/usr/local/kor/config/" #线上配置xml文件目录
def stop_server(host="",server_name=""):
    '''kill specified server
    '''
    #print "entering stop_server"
    process_name=server_name.capitalize() + "Server"
    with cd(server_dest_path + "/" + server_name):
        sudo("touch stop")
    with hide('running', 'stdout', 'stderr'):
        running = sudo("pgrep \"^%s$\" |wc -l" % process_name)
    if running != "0":
        sudo("killall -9 %s" % process_name)
    else:
        pass

def start_server(host="",server_name=""):
    '''start specified server
    '''
    #print "entering start_server"
    process_name=server_name.capitalize() + "Server"
    with hide('running', 'stdout', 'stderr'):
        running = sudo("pgrep \"^%s$\" |wc -l" % process_name)
    if running != "0":
        print "%s already running" % process_name
        return 0
    else:
        with cd(server_dest_path + "/" + server_name):
            with hide('running', 'stdout', 'stderr'):
                exist_restart=sudo("if test -e restart.sh -a -x restart.sh;then echo True;else echo False;fi" )
                exist_stop=sudo("if test -e stop;then echo True;else echo False;fi" )
            if exist_stop == "True": 
                sudo("rm stop")
            else:
                pass
            if exist_restart == "True":
                sudo('./restart.sh')
                print "starting %s ...." % process_name
            else:
                print "starting %s ...." % process_name
                with hide('running', 'stdout', 'stderr'):
                    #FIXME  without restart.sh if server can be start
                    sudo("ulimit -c 4096000;:>./%s.run.log;:>./%s.error.log;./%s 1>./%s.run.log 2>./%s.error.log &" %(server_name,server_name,process_name,server_name,server_name))
                return 0

def restart_server(host="",server_name=""):
    #print "entering restar_server"
    stop_server(server_name=server_name)
    time.sleep(3)
    start_server(server_name=server_name)

def rm_so(host="",server_name=""):
    '''delete the so file and touch file ./stop
    '''

    #print "entering rm_so"
    root_dir=os.path.dirname(server_dest_path.rstrip('/'))
    with hide('running', 'stdout', 'stderr'):
        sudo("chgrp -R %s %s" %(env.user,root_dir))
        sudo("chmod -R 775 %s" % root_dir)
    local_path = server_src_path + server_name
    dest_path = server_dest_path + server_name
    with hide('running', 'stdout', 'stderr'):
        exist=sudo("if test -e %s/%s.so;then echo True;else echo False;fi" %(dest_path,server_name))
    if exist == "True":
        with cd(dest_path):
            sudo("mv %s/%s.so{,.bak}" %(dest_path,server_name))
    else:
        pass

def upload_file(host="",server_name="" ):
    '''upload file 
    '''

    #print "entering upload_file"
    local_path = server_src_path + server_name
    dest_path = server_dest_path + server_name
    if os.path.exists(local_path):
        put("%s/*.xml" % xml_src_path,xml_dest_path)
        with hide('stdout', 'stderr'):
            with lcd(local_path):
                local("tar czvf %s.tar.gz %s.so" %(server_name,server_name),capture=False)
            put("%s/%s.tar.gz" %(local_path,server_name),dest_path)
            with cd(dest_path):
                sudo("tar xzvf %s.tar.gz" % server_name)
    else:
        pass
#服务器用户名密码
def version_update(host="",server_name="",user="user",passwd="111111"):
    env.host_string = host 
    env.user = user
    env.password = passwd
    rm_so(server_name=server_name)
    upload_file(server_name=server_name)
    stop_server(server_name=server_name)
    #start_server(server_name=server_name)

if __name__ == '__main__':
#服务器列表:
    try:
        server_dict={
            "world":["192.168.1.233:12324","192.168.1.245:12324","192.168.1.249:12324"],
            "race":["192.168.1.241:12324","192.168.1.250:12324"],
            "garage":["192.168.1.251:12324"],
            #"dir":["192.168.1.239:12324"],
            "social":["192.168.1.240:12324"],
            "tour":["192.168.1.243:12324"],
        }
#social最后一个被杀掉，第一个被启起来
        server_list=server_dict.keys()
        server_list.remove('social')
    except:
        print "请检查server_dict的格式"
        sys.exit(1)
#更新除social外的其他服务
    for server in server_list:
        for host in server_dict[server]:
            version_update(host=host,server_name=server,passwd='111111')
#更新social服务并启动
    for host in server_dict['social']:
        version_update(host=host,server_name='social')
        start_server(host=host,server_name='social')
#启动除social外的其他服务
    for server in server_list:
        for new_host in server_dict[server]:
            env.host_string = new_host 
#服务器用户名密码:
            env.user = "user"
            env.password = "111111"
            start_server(host=new_host,server_name=server)
