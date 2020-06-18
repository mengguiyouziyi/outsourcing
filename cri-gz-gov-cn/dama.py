# -*- coding: UTF-8 -*-
# ***********************************************
# **  file：     dama.py
# **  purpose：  使用云打码：题分换算：100,000题分=100元 比如4位英文验证码举例，1个码(整张图片4个英文)=1分钱
#                qq超人打码：6块钱10000点  打码一次10点好像
# **
# **  author:    mengguiyouziyi
# **  date:      2018/12/04
# ***********************************************

import requests
import os

sess = requests.session()
headers = {
    'accept': "application/json, text/javascript, */*; q=0.01",
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundaryEKaAknkxdoenjwz8",
    'origin': "http://www.yundama.com",
    'referer': "http://www.yundama.com/demo.html",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
# url = 'http://api.yundama.net:5678/api.php?method=upload'
# pic = open('./easy_img/5B6EE8BB44C9966B289ECA74A877FD40C3A5277143FA6CC6FB45FF31E2273FB3.gif', 'rb').read()
# # data = "------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"file\"\r\n\r\n{}\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nmengguiyouziyi\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nsunlijian3646287\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"codetype\"\r\n\r\n5000\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"appid\"\r\n\r\n1\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"appkey\"\r\n\r\n22cc5376925e9387a23cf797cb9ba745\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"timeout\"\r\n\r\n60\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"version\"\r\n\r\nYAPI/WEB v1.0.0\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8\r\nContent-Disposition: form-data; name=\"showimage\"\r\n\r\n1\r\n------WebKitFormBoundaryEKaAknkxdoenjwz8--".format(pic)
#
# data = """
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="file"; filename="5B6EE8BB44C9966B289ECA74A877FD40C3A5277143FA6CC6FB45FF31E2273FB3.gif"
# Content-Type: image/gif
#
# {}
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="username"
#
# mengguiyouziyi
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="password"
#
# sunlijian3646287
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="codetype"
#
# 5000
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="appid"
#
# 1
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="appkey"
#
# 22cc5376925e9387a23cf797cb9ba745
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="timeout"
#
# 60
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="version"
#
# YAPI/WEB v1.0.0
# ------WebKitFormBoundaryEKaAknkxdoenjwz8
# Content-Disposition: form-data; name="showimage"
#
# 1
# ------WebKitFormBoundaryEKaAknkxdoenjwz8--
# """.format(pic)
# res = sess.post(url, headers=headers, data=data)
# print(res.request.body)

# 请求的接口url
url = "http://api.yundama.net:5678/api.php?method=upload"

# 假设待上传文件与脚本在同一目录下
dir_path = os.path.abspath(os.path.dirname(__file__))
# 待上传文件的路径，这里假设文件名为test.txt
file_path = os.path.join(dir_path, 'easy_img', '1555495016(1).jpg')

'''
    field_1,field_2...field_n代表普通字段名
    value_1,value_2...value_n代表普通字段值
    files为文件类型字段

    实际应用中字段名field_n均需要替换为接口抓包得到的实际字段名
    对应的字段值value_n也需要替换为接口抓包得到的实际字段值
'''
files = {
    'username': (None, 'mengguiyouziyi'),
    'password': (None, 'sunlijian3646287'),
    'codetype': (None, '5000'),
    'appid': (None, '1'),
    'appkey': (None, '22cc5376925e9387a23cf797cb9ba745'),
    'timeout': (None, '60'),
    'version': (None, 'YAPI/WEB v1.0.0'),
    'showimage': (None, '1'),
    'file': (
        '1555495016(1).jpg', open(file_path, 'rb'), 'text/plain'),
}

r = sess.post(url, files=files)
print(r.text)
