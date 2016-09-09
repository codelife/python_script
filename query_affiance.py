#!/usr/bin/python
# encoding=utf-8
import time
import requests
import subprocess
import sys
query_urls = ['http://blog.sina.com.cn/s/articlelist_3260926015_0_1.html',
              'http://www.yanglee.com/studio/InfoList.aspx?NodeCode=1050241']


def query(url):
    try:
        headers = {'Referer': url,
                   'User-Agent': '(Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                   }
        end_day = time.strftime('%Y-%m-%d', time.localtime())
        query_data = {'start_date': start_day, 'end_date': end_day, 'platid': 0,'gameid': ' '}
        last_query_day = end_day
        ret_query = requests.post(QUERY_URL, headers=headers, cookies=cookies, data=query_data)
        if not ret_query.content:
            return false
        else:
            ret = ret_query.json()
            if ret['status'] == 0:
                return ret['message'].encode('utf-8')
            else:
                table = to_table(ret['data'])
                return (table, last_query_day)
    except:
        return '程序查询数据错误'


def write_to_execel(line):
    '''
    把行内容按标题写入excel
    '''
    pass


def running():
    '''
        程序是否在运行
    '''
    filename = sys.argv[0][sys.argv[0].rfind('/')+1:]
    cmdline = 'ps aux |egrep "python.* ' + filename + '"|grep -v grep |wc -l'
    ret = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = ret.communicate()
    output = int(output)
    if output == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    if running():
        print 'alreay running'
        sys.exit()
    for url in query_urls:
        contents = query(url)
    for line in contents:
        write_to_execel(line)
