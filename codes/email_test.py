__author__ = 'JunSong<songjun54cm@gmail.com>'
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# smtp_server = 'smtp.163.com'
# smtp_port = 25
# from_addr = 'songjun_toolkit@163.com'
# from_passwd = 'songjun1234'

smtp_server = 'smtp.qq.com'
smtp_port = 587
from_addr = 'songjun_toolkit@foxmail.com'
from_passwd = 'toolkitsongjun1234'

server = smtplib.SMTP(smtp_server, smtp_port)
server.login(from_addr, from_passwd)

to_addrs = 'songjun54cm@foxmail.com'
msg = MIMEText('tomorrow i will be there', 'plain', 'utf-8')
msg['Subject'] = Header('Hello SongJun ToolKit', 'utf-8')#subject
msg['From'] = from_addr
msg['To'] = to_addrs
server.sendmail(from_addr, to_addrs, msg.as_string())
