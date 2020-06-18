#!/usr/bin/env python
# coding: utf-8
# author: slj
"""
查看用法：python tradesparq.py -h
完整命令：python tradesparq.py -t website -r WZ2019.csv -s 1 -l 100 -R 4
    -t: 需要查询的类型
    -r: 需要读取的文件
    -s: 比如从 10 断了，但是已经有了前面10个文件，不想在从1开始抓取，就可以输入10，会从读取文件的第10行开始抓取。默认从1开始。
    -l: 每次查询次数，如果不输入，表示没有次数限制
    -R: 可调节，默认为4次，就是失败4次，就会执行下一行抓取，且本次失败序号会写入 tradesparq\FAIL\timestamp.fail 文件
"""

import os
import csv
import requests
import datetime
import time
import random
import argparse
import logging
import re
from PIL import Image

parse = argparse.ArgumentParser()
parse.add_argument('-t', '--query-type', dest='qtype', help='查询类型', default='website',
                   choices=['website', 'company', 'social'])
parse.add_argument('-r', '--read-file', dest='rfile_name', help='读取文件', default='WZ2019.csv')
parse.add_argument('-s', '--start', dest='start', help='查询位置序号', default='1')
parse.add_argument('-l', '--limit', dest='limit', help='一次查询条数', default='0')
parse.add_argument('-R', '--retry-times', dest='retry_times', help='失败后重试次数', default='4')
args = parse.parse_args()
qtype = args.qtype
rfile_name = args.rfile_name
start = int(args.start)
limit = int(args.limit)
retry_times = int(args.retry_times)

s = requests.session()
dt = datetime.datetime.now()
ts = int(time.mktime(time.strptime(dt.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")))
dt_format = dt.strftime('%Y-%m-%d_%H-%M-%S')

bpath = os.getcwd()
fail = os.path.join(bpath, r'FAIL')
log = os.path.join(bpath, r'LOG')
wz = os.path.join(bpath, r'TEM', r'WZ')
wzjg = os.path.join(bpath, r'TEM', r'WZJG')

uas = [
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A432',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
ups = [
    {'username': '13454707235', 'password': '12121#abc1'},
    # {'username': '18510168485', 'password': '3646287'}
]

zhc = re.compile(r'[\u4e00-\u9fa5]')

fail_file = os.path.join(fail, str(ts) + '.fail')


def get_logger():
    logger = logging.getLogger('tradesparq')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(log, f"log_{ts}.log"))

    console = logging.StreamHandler()
    formatter = logging.Formatter(
        # fmt='%(asctime)s [%(name)s] <%(levelname)s>: %(message)s',
        fmt='%(asctime)s <%(levelname)5s>: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


logger = get_logger()


def getPic():
    url = 'http://so.tradesparq.com/tradespider2/captcha?_time=1568704857634'
    res = s.get(url)
    with open(f'./pics/captcha.jpg', 'wb') as pic:
        pic.write(res.content)


"""
# no use
def getCaptcha(pic='captcha.jpg'):
    # headers = {
    #     'accept': "application/json, text/javascript, */*; q=0.01",
    #     'content-type': "multipart/form-data; boundary=----WebKitFormBoundaryEKaAknkxdoenjwz8",
    #     'origin': "http://www.yundama.com",
    #     'referer': "http://www.yundama.com/demo.html",
    #     'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    # }
    url = "http://api.yundama.net:5678/api.php?method=upload"
    # 假设待上传文件与脚本在同一目录下
    dir_path = os.path.abspath(os.path.dirname(__file__))
    # 待上传文件的路径，这里假设文件名为test.txt
    file_path = os.path.join(dir_path, 'pics', pic)

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
            pic, open(file_path, 'rb'), 'text/plain'),
    }

    r = requests.post(url, files=files)
    print(r.text)
    return r.text
"""


def login(captcha):
    # url = "http://so.tradesparq.com/tradespider2/html/login.html"
    url = 'http://so.tradesparq.com/tradespider2/user/login'
    up = random.choice(ups)
    payload = f"username={up.get('username')}&password={up.get('password')}&captcha={captcha}"
    headers = {
        'accept': "*/*",
        'origin': "http://so.tradesparq.com",
        'x-requested-with': "XMLHttpRequest",
        # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'user-agent': random.choice(uas),
        'content-type': "application/x-www-form-urlencoded",
        'Host': 'so.tradesparq.com',
        'Referer': 'http://so.tradesparq.com',
    }
    res = s.request("POST", url, data=payload, headers=headers)


def getCaptcha():
    getPic()
    img = Image.open(f'./pics/captcha.jpg')
    img.show()
    captcha = input('Plese input the captcha: ')
    return captcha


def getEmail(cookies, qtype='website', key_word=''):
    """

    :param s:
    :param qtype:
    :param key_word:
    :return:
    """
    if qtype == 'website':
        query_type = 'query'
    elif qtype == 'company':
        query_type = 'companyquery'
    elif qtype == 'social':
        query_type = 'socialQuery'
    else:
        logger.error('Plese input right query type![website,company,social]')
        return
    url = f"http://so.tradesparq.com/tradespider2/search/{query_type}"

    querystring = {"param": key_word}
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'user-agent': random.choice(uas),
        'content-type': "application/json",
        # 'Cookie': 'JSESSIONID=52C21D8EEE80BEF9438535F3A043040F; UM_distinctid=169e6841f01456-088221334685f6-3d644509-1fa400-169e6841f02935; CNZZDATA1261150668=894456160-1554345675-%7C1554345675; spider2user=13454707235; spider2session=5383; spider2session5383=52C21D8EEE80BEF9438535F3A043040F; rolename=%E4%B8%AA%E4%BA%BA%E7%89%88; userparentid=%E6%97%A0; tradespiderpermission=subuser',
        'Host': 'so.tradesparq.com',
        'Referer': 'http://so.tradesparq.com/tradespider2/html/home_result.html'
    }

    response = s.request("GET", url, headers=headers, params=querystring, cookies=cookies).json()
    emails = response.get('emails', [])
    if not emails:
        logger.error('       ' + 'Get back info: ' + str(response))
        return
    logger.info('   ' + 'email-number: ' + str(len(emails)))
    # dict_list = []
    ls = []
    for email in emails:
        myemail = email.get('name', '')
        myname = myemail.split('@')[0] if myemail else ''
        if qtype == 'social':
            staffs = email.get('staffs', [])
            if staffs and staffs[0].get('origin', '') == 'linkedin':
                mylevel = 'A'
            else:
                mylevel = 'C'
        else:
            level = email.get('level', 0)
            if level == 1:
                mylevel = 'A'
            elif level == 2:
                mylevel = 'B'
            else:
                mylevel = 'C'
        # dict_list.append({'昵称': myname, '邮箱': myemail, '等级': mylevel})
        ls.append([myname, myemail, mylevel])
    return ls


def main(qtype, rfile_name, start=1, limit=0, retry_times=2):
    """

    :param qtype:
    :param rfile_name:
    :param start:
    :param retry_times:
    :return:
    """
    if qtype not in ['website', 'company', 'social']:
        logger.error('Plese input right query type![website,company,social]')
        exit()

    captcha = getCaptcha()
    login(captcha)
    cookies = s.cookies.get_dict()

    rfile = open(os.path.join(wz, rfile_name), 'r', encoding='utf-8')
    rfile_reader = csv.reader(rfile)

    i = 0
    loop_times = 0
    for item in rfile_reader:
        if zhc.findall(item[0]):  # 有标题栏，中文
            continue
        i = i + 1
        if i < start:
            continue
        loop_times += 1
        if loop_times > limit > 0:
            # wfile.close()
            # os.remove(wfile_name)
            logger.info('Loop %d times, exit!' % limit)
            rfile.close()
            exit()

        logger.info(str(i) + '  ' + item[0] + ', ' + item[1])
        try:
            if item[0].strip():
                wfn = (item[0] + '_' + dt_format + '.csv').strip()
            else:
                wfn = (str(i) + '_' + dt_format + '.csv').strip()

            try:
                wfile_name = os.path.join(wzjg, qtype, wfn)
                wfile = open(wfile_name, 'a', encoding='utf-8', newline='')
            except:
                wfn = (str(i) + '_' + dt_format + '.csv').strip()
                wfile_name = os.path.join(wzjg, qtype, wfn)
                logger.error('       ' + 'File name is lawlessness, instead of: ' + str(wfn))
                wfile = open(wfile_name, 'a', encoding='utf-8', newline='')

            wfile_writer = csv.writer(wfile)
            wfile_writer.writerow(['昵称', '邮箱', '等级'])

            item[0] = item[0].replace('http://', '').replace('https://', '')
            ls = getEmail(cookies, qtype, item[0])
            rt = 0
            while not ls:
                rt += 1
                if rt > retry_times:
                    wfile.close()
                    os.remove(wfile_name)
                    logger.error('       ' + 'Pass! Plese check where\'s wrong!')
                    with open(fail_file, 'a', encoding='utf-8') as ff:
                        ff.write(str(i) + '\n')
                    break

                logger.error(f'      ' + f' Retry {rt} times!')
                wfile.close()
                os.remove(wfile_name)

                captcha = getCaptcha()
                login(captcha)
                cookies = s.cookies.get_dict()
                wfile = open(wfile_name, 'a', encoding='utf-8', newline='')
                wfile_writer = csv.writer(wfile)
                wfile_writer.writerow(['昵称', '邮箱', '等级'])
                ls = getEmail(cookies, qtype, item[0])

            if not ls:
                continue
            for l in ls:
                wfile_writer.writerow(l)
            wfile.close()
            time.sleep(random.randint(20, 70))
        except KeyboardInterrupt as e:
            wfile.close()
            os.remove(wfile_name)
            logger.info('Get keyboard inter reput, exit!')
            rfile.close()
            exit()
    rfile.close()


if __name__ == '__main__':
    main(qtype, rfile_name, start, limit, retry_times)
