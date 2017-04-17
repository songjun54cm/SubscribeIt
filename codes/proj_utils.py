__author__ = 'JunSong<songjun54cm@gmail.com>'
import os
import platform
import settings
class CheckStatus(object):
    NoNews=0
    SomeNews=1
sysstr = platform.system()
if sysstr == 'Windows':
    IsWindows = True
else:
    IsWindows = False

if IsWindows:
    proj_folder = 'D:\\projects\\SubscribeIt'
else:
    proj_folder = '../'
data_folder = os.path.join(proj_folder, 'data')
content_folder = os.path.join(data_folder, 'site_content')
site_info_list_path = os.path.join(data_folder, 'sites_info.json')

# when to check each site
check_time = {'hour': 22}

