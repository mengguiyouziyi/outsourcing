# -*- coding: UTF-8 -*-
# ***********************************************
# **  file：     smmDigitalRecognition.py
# **  purpose：  recognize encrypted numerals
# **
# **  author:    mengguiyouziyi
# **  date:      2018/12/04
# ***********************************************
import json
import base64
import requests
from selenium import webdriver
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from traceback import print_exc


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


def getPicPath(image):
    """
    get pic from local path
    unuseful
    :param image:
    :return:
    """
    file = open(image, 'rb')
    image = file.read()
    file.close()
    return base64.b64encode(image)


def getBigPicProgram():
    """
    get big picture
    unuseful
    :return:
    """
    # time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    fox = webdriver.Firefox(executable_path=r'..\geckodriver.exe')
    fox.get('https://www.smm.cn/')
    fox.maximize_window()
    # now that we have the preliminary stuff out of the way time to get that image :D
    element = fox.find_element_by_class_name('content-left-first-pirce')  # find part of the page you want image of
    png = element.screenshot_as_png
    # with open(f'SMM铜价{time_now}.png', 'wb') as out:
    #     out.write(png)
    fox.quit()
    return png


def getSmallPicProgram():
    """
    get small picture
    :return: pictures list
    """
    fox = webdriver.Firefox(executable_path=r'..\geckodriver.exe')
    # todo
    # wrong with phantomjs, not yet find out the reason
    # fox = webdriver.PhantomJS()
    try:
        fox.get('https://www.smm.cn/')
        fox.maximize_window()
        xpath_base = '//*[@class="content-left-first-pirce"]/div[2]/table/tbody/tr[{tr}]/td[{td}]'
        up_down = fox.find_element_by_xpath(xpath_base.format(tr=1, td=4)).text
        xpaths = [xpath_base.format(tr=tr, td=3) for tr in [1, 13, 17]]
        # code block for test phantomjs
        # xpngs = [fox.find_element_by_xpath(x) for x in xpaths]
        # print(xpngs)
        # pngs = [fox.find_element_by_xpath(x).screenshot_as_base64 for x in xpaths]  # for mainAPI
        pngs = [fox.find_element_by_xpath(x).screenshot_as_png for x in xpaths]
        # code block for test phantomjs
        # for j, png in enumerate(pngs):
        #     with open(f'{j}.png', 'wb') as out:
        #         out.write(png)
        return pngs, up_down
    except:
        print('get small picture failed!!')
        # print_exc()
    finally:
        fox.quit()


def digitalRecognizeApi(token, image):
    """
    get digital string in single picture

    字段	                是否必选	类型	    说明
    log_id	            是	    uint64	唯一的log id，用于问题定位
    words_result_num	是	    uint32	识别结果数，表示words_result的元素个数
    words_result	    是	    array()	定位和识别结果数组
    location	        是	    object	位置数组（坐标0点为左上角）
    left	            是	    uint32	表示定位位置的长方形左上顶点的水平坐标
    top	                是	    uint32	表示定位位置的长方形左上顶点的垂直坐标
    width	            是	    uint32	表示定位位置的长方形的宽度
    height	            是	    uint32	表示定位位置的长方形的高度
    words	            是	    string	识别结果字符串
    chars	            否	    array()	单字符结果，recognize_granularity=small时存在
    location	        是	    array()	位置数组（坐标0点为左上角）
    left	            是	    uint32	表示定位位置的长方形左上顶点的水平坐标
    top	                是	    uint32	表示定位位置的长方形左上顶点的垂直坐标
    width	            是	    uint32	表示定位定位位置的长方形的宽度
    height	            是	    uint32	表示位置的长方形的高度
    char	            是	    string	单字符识别结果
    :param token:
    :param image:
    :return:
    """
    host = f'https://aip.baidubce.com/rest/2.0/ocr/v1/numbers?access_token={token}'
    # 图像数据，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式
    # 是否定位单字符位置，big：不定位单字符位置，默认值；small：定位单字符位置
    # 是否检测图像朝向，默认不检测，即：false。可选值包括true - 检测朝向；false - 不检测朝向。朝向是指输入图像是正常方向、逆时针旋转90/180/270度。
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'recognize_granularity': 'false',
        'detect_direction': 'false'
    }
    res = requests.post(url=host, headers=headers, data={'image': image})
    result = res.json()
    try:
        return result['words_result'][0]['words']
    except:
        print('get digital error!! Again!')
        # print_exc()
    # with open("1.txt", "a") as f:
    #     for line in result["words_result"]:
    #         print(line["words"], end="")
    #         f.write(line["words"] + "\n")


def mainAPI(APP_ID, API_KEY, SECRET_KEY):
    """
    use api
    :param APP_ID:
    :param API_KEY:
    :param SECRET_KEY:
    :return:
    """
    # 1 get token
    token = getToken(APP_ID, API_KEY, SECRET_KEY)
    if not token:
        print('Failed to getting token!! Please retry!!')
        return
    # 2 get images, up_down
    images, up_down = getSmallPicProgram()
    print('Price Rise and Fall: ', up_down)
    # 3 recognize
    for image in images:
        dstrings = digitalRecognizeApi(token, base64.b64encode(image))
        if not dstrings:
            print('Program failed to run!! Please retry!!')
            mainAPI(APP_ID, API_KEY, SECRET_KEY)
            return
        print(dstrings)


def digitalRecognizeSdk(client, image):
    """ 调用数字识别 """
    result = client.numbers(image)
    try:
        return result['words_result'][0]['words']
    except:
        print('get digital error!!')
        print_exc()


def mainSDK(APP_ID, API_KEY, SECRET_KEY):
    """
    use SDK
    pip install baidu-aip
    :param APP_ID:
    :param API_KEY:
    :param SECRET_KEY:
    :return:
    """
    try:
        from aip import AipOcr
    except:
        print('`pip install baidu-aip` or `python setup.py install`')
        return

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    images, up_down = getSmallPicProgram()
    print('Price Rise and Fall: ', up_down)
    for image in images:
        dstrings = digitalRecognizeSdk(client, base64.b64encode(image))
        if not dstrings:
            print('Program failed to run!! Please retry!!')
            mainSDK(APP_ID, API_KEY, SECRET_KEY)
        print(dstrings)

    # """ 如果有可选参数 """
    # options = {}
    # options["recognize_granularity"] = "big"
    # options["detect_direction"] = "true"
    #
    # """ 带参数调用数字识别 """
    # client.numbers(image, options)


if __name__ == '__main__':
    APP_ID = '15046495'
    API_KEY = '4qCBaT0bRqn2LdmKU9ffBEKC'
    SECRET_KEY = 'pll0Muu25RVYoFcS7UbQfEYKt2Z3RALg'
    # use api
    mainAPI(APP_ID, API_KEY, SECRET_KEY)
    # use SDK
    # mainSDK(APP_ID, API_KEY, SECRET_KEY)
