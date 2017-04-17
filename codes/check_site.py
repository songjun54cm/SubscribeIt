__author__ = 'JunSong<songjun54cm@gmail.com>'
import argparse
import requests
import os
import difflib
from proj_utils import CheckStatus

def compare_content(old_conts, new_conts):
    diff = difflib.unified_diff(old_conts, new_conts, fromfile='old', tofile='new', lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']
    # removed = [line[1:] for line in lines if line[0] == '-']
    return added

def check_site_list(site_info_dict, content_folder):
    message_list = []
    success_n = 0
    failed_n = 0
    for site_name,site_info in site_info_dict.iteritems():
        print('checking site: %s' % site_name)
        chk_message, site_status = check_site(site_info, content_folder)
        if site_status:
            success_n += 1
        else:
            failed_n += 1
        if len(chk_message)>=1:
            message_list.append(chk_message)

    check_result_message, chk_status = form_result_list(message_list)
    res_message = 'Check finish, %d sites success, %d sites failed.\n%s' % (success_n, failed_n, check_result_message)
    return res_message, chk_status

def check_site(site_info, content_folder):
    site_name = site_info['site_name']
    site_url = site_info['site_url']
    try:
        res = requests.get(site_url)
        content_path = os.path.join(content_folder, '%s.txt'%site_name)
        cont = res.content
        if not os.path.exists(content_path):
            with open(content_path, 'wb') as f:
                f.write(cont)
            message = ''
            status = True
        else:
            with open(content_path, 'rb') as f:
                old_contents = f.read().splitlines()
            with open(content_path, 'wb') as f:
                f.write(cont)
            new_contents = cont.splitlines()
            diffs = compare_content(old_contents, new_contents)
            message = form_diff_message(diffs, site_info)
            status = True
    except Exception as e:
        message = form_error_message(str(e), site_info)
        status = False
    return message, status

def form_error_message(error_message, site_info):
    message = '''
        %s
        site: %s
        url: %s
        Error Message:
        %s
        %s'''%('#'*50, site_info['site_name'], site_info['site_url'],
             error_message, '#'*50)
    return message

def form_diff_message(diffs, site_info):
    if len(diffs) > 0:
        message = '''
            %s
            site: %s
            url: %s
            Content Additions:
            %s
            %s'''%('#'*50, site_info['site_name'], site_info['site_url'],
                 '\n'.join(diffs), '#'*50)
    else:
        message = ''
    return message

def form_result_list(chk_message_list):
    if len(chk_message_list)>0:
        message = '\n'.join(chk_message_list)
        status = CheckStatus.SomeNews
    else:
        message = 'Nothing happens, no site has any change.'
        status = CheckStatus.NoNews
    return message, status

def main(state):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='file', type=str, default='example.txt')
    args = parser.parse_args()
    state = vars(args)
    main(state)