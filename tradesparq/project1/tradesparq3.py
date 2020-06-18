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
import base64
import json
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
from CnnApp import CaptchaPredit

# 解析命令行传递的参数
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

# 一些常量
dt = datetime.datetime.now()
ts = int(time.mktime(time.strptime(dt.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")))
dt_format = dt.strftime('%Y-%m-%d_%H-%M-%S')
uas = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
]
ups = [
    {'username': '13454707235', 'password': '12121#abc1'},
    # {'username': '18510168485', 'password': '3646287'}
]
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
login_headers = {
    'accept': "*/*",
    'origin': "http://so.tradesparq.com",
    'x-requested-with': "XMLHttpRequest",
    # 'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'user-agent': random.choice(uas),
    'content-type': "application/x-www-form-urlencoded",
    'Host': 'so.tradesparq.com',
    'Referer': 'http://so.tradesparq.com',
}
zhc = re.compile(r'[\u4e00-\u9fa5]')
# cnn_url = 'http://{ip}:{port}/zqsx'.format(ip='127.0.0.1', port='8007')  # 改为你要请求的url

# 脚本用到的路径
bpath = os.getcwd()
fail = os.path.join(bpath, r'FAIL')
log = os.path.join(bpath, r'LOG')
wz = os.path.join(bpath, r'TEM', r'WZ')
wzjg = os.path.join(bpath, r'TEM', r'WZJG')
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

sess = requests.session()
captchaTrain = CaptchaPredit(r"D:\MyPackage\MyProject\model\\")


def getPic():
    """
    获取验证码图片并保存
    :return:
    """
    res = sess.get('http://so.tradesparq.com/tradespider2/captcha?_time=1568704857634')
    with open(f'./pics/captcha.jpg', 'wb') as pic:
        pic.write(res.content)


def login(captcha):
    """
    登录
    :param captcha:
    :return:
    """
    # url = "http://so.tradesparq.com/tradespider2/html/login.html"
    url = 'http://so.tradesparq.com/tradespider2/user/login'
    up = random.choice(ups)
    payload = f"username={up.get('username')}&password={up.get('password')}&captcha={captcha}"
    res = sess.request("POST", url, data=payload, headers=login_headers).json()
    return res


def getCaptchaInput():
    """
    手动输入验证码，非启用状态
    :return:
    """
    getPic()
    img = Image.open(r'./pics/captcha.jpg')
    img.show()
    captcha = input('Plese input the captcha: ')
    return captcha


def getCaptchaCnnUrl():
    '''
    神经网络模型识别验证码，并返回识别结果
    :return:
    '''
    getPic()
    f = open(r'.\pics\captcha.jpg', 'rb')
    img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    data = {'img': img_str}
    json_mod = json.dumps(data)
    response_code = requests.post(url=cnn_url, data=json_mod)
    captcha = response_code.text.replace('_', '')
    print('自动识别验证码为：' + captcha)
    return captcha


def getCaptchaCnnModel():
    '''
    神经网络模型识别验证码，并返回识别结果
    :return:
    '''
    getPic()
    f = open(r'.\pics\captcha.jpg', 'rb')
    # img_byte = base64.b64encode(f.read())
    # img_str = img_byte.decode('ascii')
    # img_byte = base64.b64decode(img_str)
    response_code = captchaTrain.predictCaptcha(f.read())
    f.close()
    captcha = response_code.replace('_', '')
    print('自动识别验证码为：' + captcha)

    return captcha


def insureLogin():
    """
    根据登陆后返回的状态来确保登录成功
    :return:
    """
    res = login(captcha=getCaptchaCnnModel())
    rt = 0
    while res.get('status', '') != '0':
        rt += 1
        if rt > 5:
            print(res)
            print('重复登录次数超过5次，请检查出错原因！退出！')
            exit()
        print('重复登录···')
        res = login(captcha=getCaptchaCnnModel())
    print('登录成功！')


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

    try:
        response = sess.request("GET", url, headers=headers, params=querystring, cookies=cookies)
        emails = response.get('emails', [])
    except Exception as e:
        logger.error('  ' + 'Get back info: ' + str(e))
        return
    finally:
        print(response)
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


def main(qtype, rfile, start=1, limit=0, retry_times=2):
    """

    :param qtype:
    :param rfile_name:
    :param start:
    :param retry_times:
    :return:
    """
    insureLogin()
    print('开始抓取···')
    cookies = sess.cookies.get_dict()

    loop_times = 0  # 总抓取次数
    i = 0
    for item in csv.reader(rfile):
        # 略过中文标题
        if zhc.findall(item[0]):  # 有标题栏，中文
            continue
        i = i + 1
        # 从给定的start位置开始抓取
        if i < start:
            continue
        # 限制每日抓取次数
        loop_times += 1
        if loop_times > limit > 0:
            # wfile.close()
            # os.remove(wfile_name)
            logger.info('Loop %d times, exit!' % limit)
            rfile.close()
            exit()

        logger.info(str(i) + '  ' + item[0] + ', ' + item[1])

        try:
            try:
                wfn = (str(i) + '_' + item[0] + '_' + dt_format + '.csv').strip()
                wfile_name = os.path.join(wzjg, qtype, wfn)
                wfile = open(wfile_name, 'a', encoding='utf-8', newline='')
            except:
                wfn = (str(i) + '_' + 'null' + '_' + dt_format + '.csv').strip()
                wfile_name = os.path.join(wzjg, qtype, wfn)
                wfile = open(wfile_name, 'a', encoding='utf-8', newline='')
                # logger.error('       ' + 'File name is lawlessness, instead of: ' + str(wfn))

            wfile_writer = csv.writer(wfile)
            wfile_writer.writerow(['昵称', '邮箱', '等级'])

            item[0] = item[0].replace('http://', '').replace('https://', '')
            ls = getEmail(cookies, qtype, item[0])
            rt = 0
            while not ls:
                # 失败次数超过限制，记录并跳过，关闭写文件，并移除
                rt += 1
                if rt > retry_times:
                    wfile.close()
                    os.remove(wfile_name)
                    logger.error('  ' + '忽略此项，请查看出错原因！')
                    with open(fail_file, 'a', encoding='utf-8') as ff:
                        ff.write(str(i) + '\n')
                    break
                logger.error(f'  ' + f'Retry {rt} times!')
                wfile.close()
                os.remove(wfile_name)

                # 重新登录
                insureLogin()
                print('开始抓取···')
                cookies = sess.cookies.get_dict()

                wfile = open(wfile_name, 'a', encoding='utf-8', newline='')
                wfile_writer = csv.writer(wfile)
                wfile_writer.writerow(['昵称', '邮箱', '等级'])
                ls = getEmail(cookies, qtype, item[0])

            if not ls:
                continue
            for l in ls:
                wfile_writer.writerow(l)
            wfile.close()
            time.sleep(random.randint(2, 10))
        except KeyboardInterrupt as e:
            wfile.close()
            os.remove(wfile_name)
            # logger.info('Get keyboard inter reput, exit!')
            logger.info('用户中断程序，退出！')
            rfile.close()
            exit()


if __name__ == '__main__':
    if qtype not in ['website', 'company', 'social']:
        logger.error('Plese input right query type![website,company,social]')
        exit()
    rfile = open(os.path.join(wz, rfile_name), 'r', encoding='utf-8')
    main(qtype, rfile, start, limit, retry_times)
    rfile.close()
