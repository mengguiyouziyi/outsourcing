import requests
from PIL import Image


def test_csv():
    import csv

    dic = {'fengju': 25, 'wuxia': 26}
    csv_file = open('testdata1.csv', 'w', newline='')
    writer = csv.writer(csv_file)
    for key in dic:
        writer.writerow([key, dic[key]])
    csv_file.close()


def test_getpic():
    import requests

    url = 'http://so.tradesparq.com/tradespider2/captcha?_time=1568704857634'
    headers = {
        'accept': "image/webp,image/apng,image/*,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'connection': "keep-alive",
        # 'cookie': "JSESSIONID=0B21DBD16296237E3776DA7EEE2C6CB7; UM_distinctid=16d3e0271e93f0-0d26a5890531bc-7c19364c-1fa400-16d3e0271ea202; CNZZDATA1261150668=106176745-1568701984-%7C1568701984; rolename=%E4%B8%AA%E4%BA%BA%E7%89%88; userparentid=%E6%97%A0; spider2user=\"\"; spider2session=\"\"; spider2session5383=\"\"",
        'host': "so.tradesparq.com",
        'referer': "http://so.tradesparq.com/tradespider2/html/login.html",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
    }

    res = requests.get(url, headers=headers)
    with open(f'./pics/captcha.png', 'wb') as pic:
        pic.write(res.content)
    return res.content


def getPic():
    url = 'http://so.tradesparq.com/tradespider2/captcha?_time=1568704857634'
    headers = {
        'accept': "image/webp,image/apng,image/*,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'connection': "keep-alive",
        # 'cookie': "JSESSIONID=0B21DBD16296237E3776DA7EEE2C6CB7; UM_distinctid=16d3e0271e93f0-0d26a5890531bc-7c19364c-1fa400-16d3e0271ea202; CNZZDATA1261150668=106176745-1568701984-%7C1568701984; rolename=%E4%B8%AA%E4%BA%BA%E7%89%88; userparentid=%E6%97%A0; spider2user=\"\"; spider2session=\"\"; spider2session5383=\"\"",
        'host': "so.tradesparq.com",
        'referer': "http://so.tradesparq.com/tradespider2/html/login.html",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
    }
    res = requests.get(url, headers=headers)
    with open(f'./pics/captcha.jpg', 'wb') as pic:
        pic.write(res.content)


def login(sess, captcha):
    # url = "http://so.tradesparq.com/tradespider2/html/login.html"
    url = 'http://so.tradesparq.com/tradespider2/user/login'
    up = {'username': '13454707235', 'password': '12121#abc1'}
    payload = f"username={up.get('username')}&password={up.get('password')}&captcha={captcha}"
    headers = {
        'accept': "*/*",
        'origin': "http://so.tradesparq.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'Host': 'so.tradesparq.com',
        'Referer': 'http://so.tradesparq.com',
    }
    res = sess.request("POST", url, data=payload, headers=headers)
    print(sess.cookies.get_dict())
    print(res.cookies.get_dict())
    return sess


def getSession():
    getPic()
    fp = open(f'./pics/captcha.jpg', 'rb')
    img = Image.open(fp)
    img.show()
    captcha = input('Plese input the captcha: ')
    fp.close()
    sess = requests.session()
    s = login(sess, captcha)
    return s


def test_(s):
    url = "http://so.tradesparq.com/tradespider2/search/companyquery"
    querystring = {"param": "搜狐"}
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
        'content-type': "application/json",
        # 'Cookie': 'JSESSIONID=08A27DD61372629589E885F874A74F72; UM_distinctid=16d3e0271e93f0-0d26a5890531bc-7c19364c-1fa400-16d3e0271ea202; userparentid=%E6%97%A0; tradespiderpermission=free1; spider2session5403=""; rolename=%E4%B8%AA%E4%BA%BA%E7%89%88; spider2user=13454707235; spider2session=5383; spider2session5383=08A27DD61372629589E885F874A74F72; CNZZDATA1261150668=106176745-1568701984-%7C1569559318'
        # 'Cookie': ''
    }
    cookies = s.cookies.get_dict()
    response = s.request("GET", url, headers=headers, params=querystring, cookies=cookies)

    print(response.text)


def wanzhengguocheng():
    s = requests.session()
    print(s.cookies.get_dict())
    with open(f'./pics/captcha.jpg', 'wb') as pic:
        pic.write(s.get('http://so.tradesparq.com/tradespider2/captcha?_time=1568704857634').content)
    Image.open(f'./pics/captcha.jpg').show()
    res = s.post(url='http://so.tradesparq.com/tradespider2/user/login',
                 data=f"username=13454707235&password=12121#abc1&captcha={input('input: ')}",
                 headers={
                     'accept': "*/*",
                     'origin': "http://so.tradesparq.com",
                     'x-requested-with': "XMLHttpRequest",
                     'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
                     'content-type': "application/x-www-form-urlencoded",
                     'Host': 'so.tradesparq.com',
                     'Referer': 'http://so.tradesparq.com',
                 })
    print(s.cookies.get_dict())
    print(res.cookies.get_dict())
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
        'content-type': "application/json",
    }
    cookies = s.cookies.get_dict()
    response = s.get(url="http://so.tradesparq.com/tradespider2/search/companyquery?param=搜狗", headers=headers,
                     cookies=cookies)

    print(response.text)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    img = Image.open(f'./pics/captcha.jpg')
    plt.figure(figsize=(4, 4))
    plt.ion()  # 打开交互模式
    plt.axis('off')  # 不需要坐标轴
    plt.imshow(img)
    # pylab.show()
    # mngr = plt.get_current_fig_manager()
    # mngr.window.wm_geometry("+380+310")  # 调整窗口在屏幕上弹出的位置
    plt.show()

    captcha = input('Plese input the captcha: ')

    plt.pause(2)  # 该句显示图片15秒
    plt.ioff()  # 显示完后一定要配合使用plt.ioff()关闭交互模式，否则可能出奇怪的问题
    plt.clf()  # 清空图片
    plt.close()  # 清空窗口
