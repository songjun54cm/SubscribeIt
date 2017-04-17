__author__ = 'JunSong<songjun54cm@gmail.com>'
import argparse, time
import datetime
import json
from proj_utils import proj_folder, data_folder, site_info_list_path, check_time
from check_site import check_site_list
import os
from send_email_message import send_email_message

def get_next_check_time(check_time):
    check_hour = check_time['hour']
    now = datetime.datetime.now()
    if now.hour >= check_hour:
        next_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1),
                                              datetime.time.min) + datetime.timedelta(hours=check_hour)
    else:
        next_time = datetime.datetime.combine(datetime.date.today(), datetime.time.min) \
                    + datetime.timedelta(hours=check_hour)
    return next_time

def wait_till_check_time(check_time):
    next_check_time = get_next_check_time(check_time)
    sleep_time = next_check_time - datetime.datetime.now()
    print('now time: %s' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('next check time: %s, wait %d days, %d seconds' %
          (next_check_time.strftime("%Y-%m-%d %H:%M:%S"), sleep_time.days, sleep_time.seconds))
    time.sleep(sleep_time.total_seconds())

def get_site_info_dict(site_list_path):
    with open(site_list_path, 'rb') as f:
        site_dict = json.load(f)
    return site_dict

def check_and_send_message(content_folder):
    print('start check sites')
    site_info_dict = get_site_info_dict(site_info_list_path)
    check_message, status = check_site_list(site_info_dict, content_folder=content_folder)
    send_email_message(check_message, status=status)
    # print 'message: '
    # print check_message
    print('message has been sent to user')

def main(state):
    content_folder = os.path.join(data_folder, 'site_content')
    check_and_send_message(content_folder)
    while True:
        wait_till_check_time(check_time)
        check_and_send_message(content_folder)
        print('sleep two hours')
        time.sleep(datetime.timedelta(hours=2).total_seconds())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='file', type=str, default='example.txt')
    args = parser.parse_args()
    state = vars(args)
    main(state)