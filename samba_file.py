#!/usr/bin/env python
#coding=utf-8
#运行条件:
    #目录及命名规则:
    #1.线上项目目录:/usr/local/kor/client/ 
    #2.ssh用户需有sudo权限
    #3.本地客户端目录下的client目录
import smbclient
import subprocess
import time
import os
import re
import sys
import shutil
global workdir 
workdir='/home/web/test.kuku01.com/'
def samba_getclient(filename,server,sharedir,username,password):
    '''get the client zip file

    
    '''
    print "file name is :" +filename
    update_dir='/patch/'              #192.168.1.247 及ftp上"共享"目录
    #sharedir must the root dir of the samba share'
    smb = smbclient.SambaClient(server=server, share=sharedir, 
                                    username=username, password=password,
                                    )
    try:
        if smb.isfile(update_dir+filename):
            print "Downloading file from %s:/patch/ ......." %server
            smb.download(update_dir+filename,workdir+os.sep+filename)
        else:
            print "No such file"
            sys.exit(1)
    except:
        print "samba connect fail"
def get_version(filename):
    fd=open(filename,'r')
    version=fd.readline().split('=')[1].strip(';')
    print "最新版本: %s" % version

def sub_str_file(filename,old,new):
    fd=open(filename,'rw+')
    all_content=fd.read()
    replaced_string=all_content.replace(old,new) 
    fd.seek(0)
    fd.truncate()
    fd.write(replaced_string)

def update_file_revision(filename,revsion_path = '/home/web/test.kuku01.com/revision.swf'):
    '''update specific file  version num
    
    '''
    fd = open(revsion_path,'r')
    tmp_fd = open(revsion_path + '.tmp','w')   
    file_regx = re.compile('[\s,|\r\n]%s[\s,\r\n]' %filename)  
    for line in fd.readlines():
        if re.search(file_regx,line):
            num =  line.split('|')[0]
            num_add = int(num) + 1  
            line =  line.replace(num,str(num_add))
        tmp_fd.write(line)
    tmp_fd.close()
    fd.close()
    os.rename(revsion_path + '.tmp',revsion_path )

        
if __name__ == '__main__':
    webroot='public'
    if len(sys.argv[:])==1:
        zip_file=raw_input("The client file name:")
    else:
        zip_file=sys.argv[1]
    samba_getclient(zip_file,'192.168.1.247','共享','collin','rage@2011')           #download file from samba
    #get uncompress dir name  and the compress type
    dir_name=zip_file.rsplit('.',1)[0]
    compress_type=zip_file.rsplit('.',1)[1]
    #Delete the previous version dir
    try:
        os.chdir(workdir)
        shutil.rmtree(dir_name)
    except:
        pass
    if compress_type=='zip':
        p=subprocess.Popen('unzip -qq -x %s' %zip_file,shell=True,cwd=workdir) 
        p.wait()
        try:
            os.chdir(workdir)
            shutil.rmtree(webroot)
        except:
            pass
        os.chdir(workdir)
        os.rename(dir_name + os.sep + 'resource'  ,webroot)
    elif compress_type=='rar':
        try:
            os.chdir(workdir)
            shutil.rmtree(webroot)
        except:
            pass
        p=subprocess.Popen('unrar x  %s ' %zip_file,shell=True,cwd=workdir) 
        p.wait()
        os.rename('resource',webroot)
    sub_str_file(workdir + webroot + os.sep + 'config/serverGroup.xml','192.168.1.250','180.168.101.74')
    update_file_revision('serverGroup.xml')
    get_version(filename=workdir+ webroot + os.sep + '/cur.js')
    os.remove(zip_file)
    sys.exit(0)
