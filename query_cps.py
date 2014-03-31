#!/usr/bin/python
# encoding=utf-8
sender = 'no_reply@ok130.com'
reciver = '1234@qq.com'

def query():
    import requests
    import re
    LOGIN_URL = 'http://www.37cs.com/login.php'
    PAY_URL = 'http://www.37cs.com/cps.php?action=income'
    POST_DATA = {'action': 'login', 'login_account':
                'foo', 'password': 'bar'}
    R_LOGIN = requests.post(LOGIN_URL, params=POST_DATA)
    R_PAY = requests.get(PAY_URL, cookies=R_LOGIN.cookies)
    patt = '<table id="my_data".*?>.*?</table>'
    TT = re.search(re.compile(patt, re.DOTALL), R_PAY.content)
    content, count = re.subn('(<th>|<td>).*?(</th>|</td>)\n\s*</tr>', '</tr>', TT.group())
    if(count >= 2):
        return content
    else:
       print '替换失败'
       return None

def mail_notify(sender, reciver, content):
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
    msg['Subject'] = '充值统计: %s' % time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
    msg['From'] = sender
    msg['To'] = reciver
    mail_content = html_wrap.replace('xxx', content.replace('border="0"', 'border="1"').replace('充值', ''))
    msg.attach(MIMEText(mail_content, 'html'))
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, reciver.split(), msg.as_string())
    s.quit()

if __name__ == '__main__':
    content = query()
    if(content):
        mail_notify(sender, reciver, content)
    else:
        print "query flase"
