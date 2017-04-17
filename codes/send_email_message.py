__author__ = 'JunSong<songjun54cm@gmail.com>'
import argparse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from proj_utils import smtp_server, smtp_port, app_email, app_passwd, user_email, CheckStatus
import datetime

def send_email_message(message, status=CheckStatus.NoNews):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(app_email, app_passwd)
    from_addr = app_email
    to_addrs = user_email
    msg = MIMEText(message, 'plain', 'utf-8')
    if status == CheckStatus.NoNews:
        status_m = 'No News.'
    elif status == CheckStatus.SomeNews:
        status_m = 'Some News.'
    else:
        status_m = 'Unknow State.'
    msg['Subject'] = Header('%s SJ-SubscribeIt-%s'%(status_m, datetime.datetime.now().date()), 'utf-8')#subject
    msg['From'] = from_addr
    msg['To'] = to_addrs
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.close()

def main(state):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='file', type=str, default='example.txt')
    args = parser.parse_args()
    state = vars(args)
    main(state)