#!/usr/bin/env python
# coding=utf-8
from fabric.api import run, env
from fabric.operations import put, local
from fabric.context_managers import *
from fabric.colors import green, red, blue, yellow
import time
import os
import sys
global ipay_nginx_host  # ipay nginx 运行的服务器
global gc_nginx_host   # gc nginx 运行的服务器
global local_war  # war包所在的目录
global local_opt  # opt文件所在的目录
global server_ip

global tomcat_root  # 远程服务器tomcat所在的目录 默认/data
global app_dir  # 远程服务器war包部署在哪个目录 webapps
local_war = '/home/production_latest/'
tomcat_root = '/data/'
app_dir = 'webapps/'
ipay_nginx_host = '3.4.5.6'
gc_nginx_host = '3.4.5.6'
server_ip = server_ip


def check_running_group(server_group):
    '''确认当前是哪一组服务器在运行
    '''
    if server_group == 'ipay':
        env.host_string = ipay_nginx_host
        conf_file = 'production_ipay.conf'
    elif server_group == 'gc':
        env.host_string = gc_nginx_host
        conf_file = 'production_gc.conf'
    else:
        print "服务器组错误, 不在['ipay', 'gc'] 范围内"
    env.user = "root"
    env.key_filename = "~/.ssh/id_rsa"
    running_group = run("head -1 /usr/local/tengine/conf/vhosts/%s | awk -F '#In use:' '{print $2}'  | awk -F '_' '{print $2}'" % conf_file)
    return running_group


def stop_server(host="", server_dir=""):
    '''停止指定的tomcat服务
    '''
    tomcat_dir = tomcat_root+server_dir
    print (green('[INFO:] Stopping : %s') % server_dir)
    with hide('running', 'stdout'):
        running = run("ps aux | grep 'Dcatalina.home=%s' | grep -v grep | wc -l " % tomcat_dir)
        if int(running) >= 1:
            pids = run("ps aux | grep 'Dcatalina.home=%s' | grep -v grep | awk '{print $2}' " % tomcat_dir)
            pids = pids.split('\r\n')
            for pid in pids:
                run("kill -9 %s " % pid)
        with cd(tomcat_root + server_dir):
            run("rm -rf work/Catalina")


def start_server(host="", server_dir=""):
    '''启动指定的tomcat服务
    '''
    # print "entering start_server"
    tomcat_dir = tomcat_root+server_dir
    with hide('running', 'stdout'):
        running = run("ps aux | grep 'Dcatalina.home=%s' | grep -v grep | wc -l " % tomcat_dir)
    if int(running) == 1:
        print (yellow('[WARN:] %s is already running') % server_dir)
        return True
    else:
        print (green('[INFO:] Starting : %s') % server_dir)
        with cd(tomcat_root + server_dir):
            with hide('running', 'stdout'):
                run("/bin/bash %s/bin/startup.sh" % tomcat_dir, pty=False)
# todo 检测catalina.out 是否有错误


def restart_server(server_dir=""):
    stop_server(server_dir=server_dir)
    start_server(server_dir=server_dir)


def rm_war(war_file="", server_dir=""):
    '''删除war包和展开的文件夹
    '''

    # print "entering rm_war"
    if '-gc.war' in war_file:
        war_file = war_file.replace('-gc', '')
    with cd(tomcat_root + server_dir + '/' + app_dir):
        run("rm -rf ./%s ./%s" % (war_file, war_file.split('.')[0]))


def check_if_updated(host="", war_file="", server_dir=""):
    ''' 检查是否已经是最新文件, 已经是最新的跳过更新
    '''
    if '-gc.war' in war_file:
        remote_file = tomcat_root + server_dir + '/' + app_dir + war_file.replace('-gc', '')
    else:
        remote_file = tomcat_root + server_dir + '/' + app_dir + war_file
    with lcd(local_war):
        with hide('running', 'stdout'):
            local_size = local("stat -c %%s %s " % war_file, capture=True)
            remote_size = run("stat -c %%s %s " % remote_file)
            if(local_size != remote_size):
                return False
            local_md5 = local("md5sum %s | awk '{print $1}'" % war_file, capture=True)
            remote_md5 = run("md5sum %s | awk '{print $1}'" % remote_file)
        if local_md5 == remote_md5:
            print(green('[INFO:] %s is already is latest version ,skip update' % war_file))
            return True
        else:
            return False


def upload_file(host="", war_file='', server_dir=''):
    '''上传war包'''
    # print "entering upload_file"
    with hide('stdout', 'stderr'):
        with lcd(local_war):
            put(war_file, tomcat_root + server_dir + '/' + app_dir)
        if '-gc' in war_file:  # 特殊处理gc相关的文件
            with cd(tomcat_root + server_dir + '/' + app_dir):
                run("mv %s %s" % (war_file, str.join('', war_file.split('-gc'))))


def update(host='', war_file='', server_dir='', user="root"):
    ''' 更新逻辑'''
    print(green('\n[INFO:] updating %s ' % war_file))
    with hide('running', 'stdout'):
        if_tomcat_dir_exist = run('if [ -d %s ];then echo True ;else echo False;fi' % (tomcat_root + server_dir))
    if if_tomcat_dir_exist:
        if_updated = check_if_updated(war_file=war_file, server_dir=server_dir)
        if not if_updated:
###########################更新前是否需要用户参与,不需要注释本段###############
            confirm = raw_input('更新文件%s 到主机 %s 是否继续?(Y|N):' % (war_file, host))
            if confirm != 'Y':
                return
##################################结束#########################################
            stop_server(server_dir=server_dir)  # 停止server
            rm_war(war_file=war_file, server_dir=server_dir)  # 删除war包
            upload_file(war_file=war_file, server_dir=server_dir)  # 上传war包
            start_server(server_dir=server_dir)  # 启动服务
        else:
            start_server(server_dir=server_dir)  # 如果war包已经是最新的,跳过更新 启动服务
    else:
        print(red('[ERROR:] tomcat目录%s不存在)' % (tomcat_root + server_dir)))

if __name__ == '__main__':
    hostname = socket.gethostname()
    if hostname != 'hkbank':
        print '指定的机器运行, 防止维护人员的主机已添加key,自动运行'
        sys.exit(1)
    # todo 判断现在用的是哪一组server, 需要更新的是哪个哪一组服务

# 服务器列表:
    try:
        war_dict_ipay = {
            'accounting.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-accounting'},
            'poss.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-poss'},
            # 'if-task.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-task'},
            'ma-mdbtask.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-mdb'},
            'pe-accumulated.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-mdb'},
            'fo-mdp.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-mdb'},
            'notification.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-notification'},
            'static.war': {'master': [server_ip], 'new': [server_ip], 'dir': ['tomcat-gateway','tomcat-website']},
            'webgate.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'gateway.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'channel.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'txncore.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'risk.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-cybs'},
            'cybs.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-cybs'},
            'forpay.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-forpay'},
            'wechat.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-wechat'},
            'website.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-website'},
            'ordercenter.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-ordercenter'},
        }
        war_dict_gc = {
            'accounting.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-accounting'},
            'poss.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-poss'},
            'ma-mdbtask.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-mdb'},
            'pe-accumulated.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-mdb'},
            'fo-mdp.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-mdb'},
            'notification.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-notification'},
            'static-gc.war': {'master': [server_ip], 'new': [server_ip], 'dir': ['tomcat-gateway', 'tomcat-website']},
            'webgate.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'gateway.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'channel.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'txncore.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-gateway'},
            'risk.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-cybs'},
            'cybs.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-cybs'},
            'forpay.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-forpay'},
            'wechat.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-wechat'},
            'website-gc.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-website'},
            'ordercenter.war': {'master': [server_ip], 'new': [server_ip], 'dir': 'tomcat-ordercenter'},
            'computop.war': {'master': [server_ip, server_ip], 'new': [server_ip, server_ip], 'dir': 'tomcat-cashu'},
            'callback.war': {'master': [server_ip, server_ip], 'new': [server_ip, server_ip], 'dir': 'tomcat-cashu'},
            'cashu.war': {'master': [server_ip, server_ip], 'new': [server_ip, server_ip], 'dir': 'tomcat-cashu'},
            'boleto.war': {'master': [server_ip, server_ip], 'new': [server_ip, server_ip], 'dir': 'tomcat-cashu'},
        }
    except:
        print "请检查server_dict的格式"
        sys.exit(1)

    server_groups = ['ipay', 'gc']  # 更新的服务组, 先更新ipay,后gc
    for server_group in server_groups:
        update_to_switch_group = raw_input('更新[ %s ]中的哪一组服务器(master|new):' %(server_group.upper()))
        running_group = check_running_group(server_group)

        print running_group
        # 检测tengine中的运行的哪一个组服务器.
        if running_group == update_to_switch_group:
            print (red('[ERROR:] 系统检测[ %s ]的[ %s ]正在对外服务') %(server_group.upper(), running_group))
            confirm = raw_input('[info] 系统检测[ %s ]的[ %s ]正在对外服务,确认要更新这一组服务(Y|N):' %(server_group.upper(), running_group))
            if confirm != 'Y':
                sys.exit(1)
        ################# 检测逻辑结束 ###############
        sys.exit(1)

        print(red('-----'*20))
        war_dict = eval('war_dict_' + server_group)
        for war_file in os.listdir(local_war):
            if war_file in war_dict.keys():
                server_dir = war_dict[war_file]['dir']
            else:
                print (yellow('[WARNING:] 缺少%s 文件的更新路径等信息, 跳过此文件的更新') % war_file)
                continue
            for host in war_dict[war_file][update_to_switch_group]:
                env.host_string = host
                env.user = "root"
                env.key_filename = "~/.ssh/id_rsa"
                if isinstance(server_dir, list):  # 特殊处理static 多目录
                    for single_dir in server_dir:
                        update(host=host, war_file=war_file, server_dir=single_dir)
                else:
                    update(host=host, war_file=war_file, server_dir=server_dir)
    print(green('[INFO:]  all file update success'))
