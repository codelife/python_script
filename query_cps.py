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
sender = 'no_reply@ok130.com'
#RECIVER = 'aaa61328@qq.com aaa24517@qq.com aaa2854@qq.com aaa8@qq.com '
ACCOUNT = 'account'
PASSWORD = 'password'
INDEX_URL = 'http://www.37cs.com/index.php'
LOGIN_URL = 'http://www.37cs.com/login.html'
QUERY_URL = 'http://www.37cs.com/index.php?action=User&do=manage&method=cpsincome&ajax=data'
# requests.get('http://www.37cs.com/index.php?action=Login&do=loginStatus', cookies = cookies)
def cl(image):
    image = image.convert('L')
    image = image.point(lambda x: 0 if x<158 else 255, '1')
    return image

def read(image):
    text = image_to_string(image)
    return text

def get_code():
    global vcode
    global cookies
    timestamp = str(time.time()).split('.')[0] + '000'
    vcode_data = {'action': 'Login','do': 'vcode','t': timestamp}
    r_vcode = requests.get(INDEX_URL,params = vcode_data)
    i = Image.open(StringIO(r_vcode.content))
    i.save('/home/jp2014/png/aa.png')
    gray = cl(i)
    gray.save('/home/jp2014/png/aa_de.png')
    vcode = read(gray)[0:4]
    cookies = r_vcode.cookies
    #print(tuple(r_vcode.cookies))
    print 'vcode: %s' %vcode
    print image_file_to_string('/home/jp2014/png/aa.png')
    print(cookies)

def login():
    login_data = {'user_name': ACCOUNT, 'user_pwd': PASSWORD, 'user_vcode':vcode}
    post_login = requests.post(INDEX_URL + '?action=Login&do=login', cookies=cookies,data=login_data)
    ret=post_login.json()
    print login_data
    print post_login.content
    print "ret status:%s" %ret['status']
    return ret['status']

def query():
    headers = {'Referer':'http://www.37cs.com/user.html',
            'User-Agent':'(Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'X-Requested-With':'XMLHttpRequest',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
            }
    day=time.strftime('%Y-%m-%d',time.localtime())  
    print day
    print(cookies)
    query_data = {'start_date' : day,'end_date' : day,'platid' : 0,'gameid':' '}
    ret_query = requests.post(QUERY_URL,headers=headers, cookies=cookies,data=query_data)
    print QUERY_URL
    print query_data
    print ret_query.url
    print ret_query.content
    sys.exit()
    patt = '<table id="my_data".*?>.*?</table>'
    TT = re.search(re.compile(patt, re.DOTALL), R_PAY.content)
    content, count = re.subn('(<th>|<td>).*?(</th>|</td>)\n\s*</tr>', '</tr>', TT.group())
    if(count >= 2):
        return content
    else:
       print '替换失败'
       return None

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
    mail_content = html_wrap.replace('xxx', content.replace('border="0"', 'border="1"').replace('充值', ''))
    msg.attach(MIMEText(mail_content, 'html'))
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, RECIVER.split(), msg.as_string())
    s.quit()

if __name__ == '__main__':
    login_code = 0
    #while(login_code == 0):
    get_code()
    login_code = login()
    content = query()
    if(content):
        mail_notify(sender, RECIVER, content)
    else:
        print "query flase"
