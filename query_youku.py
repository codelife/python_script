#!/usr/bin/python
# encoding=utf-8
from pprint import pprint
import sys
from PIL import Image
from StringIO import StringIO
import time
import shutil
from pytesser import *
import requests
import subprocess
sender = 'no_reply@ok130.com'
RECIVER = '123'
ACCOUNT = '123'
PASSWORD = '123'
IMGCODE_URL = 'http://123.123.225.162:8099/servlet/ticketImage?rand='
LOGIN_URL = 'http://123.123.225.162:8099/admin/login.action'
QUERY_URL = 'http://123.123.225.162:8099/admin/openAccountAuto.action'
qd_code = "D398FD199AAA424CA7CCA3CD56CC4AAB"

def cl(image):
    image = image.convert('L')
    image = image.point(lambda x: 0 if x<158 else 255, '1')
    return image


def read(image):
    text = image_to_string(image)
    return text


def get_imgcode():
    global vcode
    global cookies
    timestamp = str(time.time()).split('.')[0] + '000'
    IMGCODE_URL += timestamp
    r_vcode = requests.get(IMGCODE_URL)
    i = Image.open(StringIO(r_vcode.content))
    i.save('/tmp/qd_imgcode.png')
    gray = cl(i)
    gray.save('/tmp/qd_imgcode_de.png')
    vcode = read(gray)[0:4]
    cookies = r_vcode.cookies
    #print(tuple(r_vcode.cookies))
    print('vcode: %s' %vcode)
    #print image_file_to_string('/home/jp2014/png/aa.png')

def login():
    login_data = {'form.name': ACCOUNT, 'form.password': PASSWORD, 'ticket': vcode, 'siteno': "main"}
    post_login = requests.post(LOGIN_URL, cookies=cookies, data=login_data)
    ret = post_login.json()
    print(ret)
    time.sleep(3)
    return ret


def to_table(data):
    head = '''
    <table cellspacing="1" cellpadding="0" border="1" class="tablesorter" style="width:680px" id="my_data"> <thead> <tr> <th>日期</th> <th>游戏平台</th> <th>游戏名称</th> <th>游戏服</th> <th>人数</th> <th>金额</th> </tr> </thead> <tbody>
    '''
    body=''
    count = len(data)
    consumers=0
    money=0
    for i in range(count):
        BILL_DAY = data[i]['BILL_DAY'].encode('utf-8')
        PLATFORM_NAME =data[i]['PLATFORM_NAME'].encode('utf-8')
        GAME_NAME = data[i]['GAME_NAME'].encode('utf-8')
        SERVER_NAME = data[i]['SERVER_NAME'].encode('utf-8')
        CONSUMERS = data[i]['CONSUMERS'].encode('utf-8')
        CONSUMPTION = data[i]['CONSUMPTION'].encode('utf-8')
        body+="<tr><td><span times=\"\" t=\"5\" style=\"border-bottom:1px dashed #ccc;\">%s</span></td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> </tr><tr></tr>" %(BILL_DAY,PLATFORM_NAME,GAME_NAME,SERVER_NAME,CONSUMERS,CONSUMPTION)
        consumers += int(data[i]['CONSUMERS'])
        money += float(data[i]['CONSUMPTION'])
    body += "</tbody> <tfoot> <tr> <th align=\"center\" colspan=\"1\">总计</th> <th colspan=\"3\">&nbsp;</th> <th>%s</th> <th>%s</th> </tr> </tfoot> </table>" %(consumers, money)
    table = head + body
    return table
'''
processFront    "success"
mobileno    ""
idno    ""
custname    ""
processBack    ""
infocolect_channel    ""
opacctkind_flag    "D398FD199AAA424CA7CCA3CD56CC4AAB"
service_flag    ""
button    "%CB%D1%CB%F7"
page    "1"
'''

def query(start_day):
    try:
        headers = {'Referer': 'http://123.123.225.162:8099/admin/openAccountAuto.action?manageCatalogId=5110',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
                   'X-Requested-With': 'XMLHttpRequest',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': "keep-alive",
                   }
        query_data = {
            'form.pageUrl': "manageCatalogId=5110",
            'function': "",
            'manageCatalogId': "5110",
            'subManageCatalogId': "",
            'branch': "",
            'start_timebeg': start_day,
            'start_timeend': "",
            'id': "",
            'processFront': "success",
            'mobileno': "",
            'idno': "",
            'custname': "",
            'processBack': "",
            'infocolect_channel': "",
            'opacctkind_flag': qd_code,
            'service_flag': "",
            'button': "%CB%D1%CB%F7",
            'page': "1"}
        ret_query = requests.post(QUERY_URL, headers=headers, cookies=cookies, data=query_data)
        if not ret_query.content:
            return false
        else:
            print(ret_query.content)
# todo filter table
    except:
        return '程序查询数据错误'


def mail_notify(sender, RECIVER, content):
    html_wrap = '''
    <html>
    <head></head>
    <body>
    xxx
    </body>
    </html>
        '''
    import smtplib
    import time
    from email.MIMEMultipart import MIMEMultipart
    from email.mime.text import MIMEText
    msg = MIMEMultipart()
    msg['Subject'] = '充值统计-1: %s' % time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
    msg['From'] = sender
    msg['To'] = RECIVER
    try:
        mail_content = html_wrap.replace('xxx', content.replace('border="0"', 'border="1"'))
    except:
        mail_content = content
    msg.attach(MIMEText(mail_content, 'html'))
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, RECIVER.split(), msg.as_string())
    s.quit()


def running():
    cmdline = 'ps aux |egrep "/usr/bin/python.*query_youku.py"|grep -v grep |wc -l'
    ret = subprocess.Popen(cmdline, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = ret.communicate()
    output = int(output)
    if output == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    start_day = time.strftime('%Y-%m-%d', time.localtime())
    if not running():
        sys.exit()
    login_code = 0
    count = 0
    fail = 0
    while(login_code == 0):
        get_imgcode()
        time.sleep(3)
        login_code = login()
        content, start_day = query(start_day)
        time.sleep(60)
        #if(content):
        #    mail_notify(sender, RECIVER, content)
        #else:
        #    fail+=1
        #if(fail>3):
        #break
        #requests.get(LOGIN_STATUS_URL,cookies=cookies)
        #count+=1
