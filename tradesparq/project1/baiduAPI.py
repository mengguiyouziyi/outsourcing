# -*- coding: UTF-8 -*-
# ***********************************************
# **  file：     smmDigitalRecognition.py
# **  purpose：  recognize encrypted numerals
# **
# **  author:    mengguiyouziyi
# **  date:      2018/12/04
# ***********************************************

__author__ = 'mengguiyouziyi'

import json
import base64
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from traceback import print_exc

try:
    from aip import AipOcr
except:
    print('`pip install baidu-aip` or `python setup.py install`')

# APP_ID = '15046495'
# API_KEY = '4qCBaT0bRqn2LdmKU9ffBEKC'
# SECRET_KEY = 'pll0Muu25RVYoFcS7UbQfEYKt2Z3RALg'
APP_ID = '17265352'
API_KEY = 'Sp0PzmTG4mDSLYFbiANGWQaP'
SECRET_KEY = 'tggxw3rK623r9mxAxOg3pecHIix2CIG4'


def getToken(APP_ID, API_KEY, SECRET_KEY):
    """
    get baidu api token
    :return:
    """
    host = 'https://aip.baidubce.com/oauth/2.0/token?'
    param = {
        'grant_type': 'client_credentials',
        'client_secret': SECRET_KEY,
        'client_id': API_KEY,
    }
    host = host + urlencode(param)
    request = Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urlopen(request)
    content = response.read()
    if (content):
        result = json.loads(content)
        print(result)
        return result.get('access_token', '')


def digitalRecognizeApi(token, image):
    host = f'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={token}'
    print(host)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        # 'recognize_granularity': 'false',
        # 'detect_direction': 'false'
    }
    try:
        res = requests.post(url=host, headers=headers, data={'image': image})
        result = res.json()
        print(result)
        if result['words_result']:
            return result['words_result'][0]['words']
    except:
        print_exc()
        print('get digital error!! Again!')


def baiduAPImain(image):
    token = getToken(APP_ID, API_KEY, SECRET_KEY)
    if not token:
        print('Failed to getting token!! Please retry!!')
        return
    token = '24.639ff1cce836415275c9b76f58fe91db.2592000.1571305411.282335-17265352'
    dstrings = digitalRecognizeApi(token, base64.b64encode(image))
    if not dstrings:
        print('Program failed to run!! Please retry!!')
        return
    print(dstrings)
    return dstrings


def digitalRecognizeSdk(client, image):
    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"
    """ 调用数字识别 """
    result = client.basicGeneralUrl(image, options)
    print(result)
    try:
        return result['words_result'][0]['words']
    except:
        print('get digital error!!')
        print_exc()


def baiduSDKmain(image):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    dstrings = digitalRecognizeSdk(client, base64.b64encode(image))
    if not dstrings:
        print('Program failed to run!! Please retry!!')
        return
    print(dstrings)
    return dstrings


if __name__ == '__main__':
    with open('./pics/captcha.png', 'rb') as image:
        baiduAPImain(image.read())
