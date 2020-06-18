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

APP_ID = '15046495'
API_KEY = '4qCBaT0bRqn2LdmKU9ffBEKC'
SECRET_KEY = 'pll0Muu25RVYoFcS7UbQfEYKt2Z3RALg'


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
        return result.get('access_token', '')


def digitalRecognizeApi(token, image):
    host = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        # 'recognize_granularity': 'false',
        # 'detect_direction': 'false'
    }
    try:
        res = requests.post(url=host, headers=headers, data={'image': image})
        result = res.json()
        return result['words_result'][0]['words']
    except:
        print_exc()
        print('get digital error!! Again!')


def digitalRecognizeSdk(client, image):
    """ 调用数字识别 """
    result = client.numbers(image)
    print(result)
    try:
        return result['words_result'][0]['words']
    except:
        print('get digital error!!')
        print_exc()


def baiduAPImain(image):
    token = getToken(APP_ID, API_KEY, SECRET_KEY)
    if not token:
        print('Failed to getting token!! Please retry!!')
        return
    dstrings = digitalRecognizeApi(token, base64.b64encode(image))
    if not dstrings:
        print('Program failed to run!! Please retry!!')
        return
    print(dstrings)
    return dstrings


def baiduSDKmain(image):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    dstrings = digitalRecognizeSdk(client, base64.b64encode(image))
    if not dstrings:
        print('Program failed to run!! Please retry!!')
        return
    print(dstrings)
    return dstrings


if __name__ == '__main__':
    with open('./easy_img/866C660B46C88B591EBF1D983950F6F33F5CA7DAB699A40D07335F6410EF1893.png', 'rb') as image:
        baiduSDKmain(image.read())
