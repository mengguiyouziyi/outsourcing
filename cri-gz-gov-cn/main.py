import requests
import os, sys
from scrapy.selector import Selector
from baiduAPI import baiduAPImain, baiduSDKmain
from PIL import Image

sys.path.append('..')
sys.path.append('../..')

sess = requests.session()


def getGuid():
    url = 'http://cri.gz.gov.cn/Search/NewGuid?t=1555470469790'
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'host': "cri.gz.gov.cn",
        'proxy-connection': "keep-alive",
        'referer': "http://cri.gz.gov.cn/Search/Result?validateCode=x69y4&guid=37EA9F0D3181E3F45839631B0F22EB3620858DC8EDEC7781439EBFA0BD41D304&keywords=440126603901334",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
    }
    guid = sess.get(url, headers=headers).text
    return guid


def getPic(guid):
    url = f'http://cri.gz.gov.cn/Search/ValidateCode?t=1555470469876&guid={guid}'

    # def down(audio):
    #     def cbk(a, b, c):
    #         '''回调函数
    #         @a: 已经下载的数据块
    #         @b: 数据块的大小
    #         @c: 远程文件的大小
    #         '''
    #         per = 100.0 * a * b / c
    #         if per > 100:
    #             per = 100
    #         print('%.2f%%' % per)
    #
    #     print('Download %s' % audio)
    #     urlretrieve(audio, f'easy_img/{guid}.jpg', cbk)
    #
    # down(url)

    headers = {
        'accept': "image/webp,image/apng,image/*,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'host': "cri.gz.gov.cn",
        'proxy-connection': "keep-alive",
        'referer': "http://cri.gz.gov.cn/Search/Result?validateCode=x69y4&guid=37EA9F0D3181E3F45839631B0F22EB3620858DC8EDEC7781439EBFA0BD41D304&keywords=440126603901334",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    }
    res = sess.get(url, headers=headers)
    with open(f'./easy_img/{guid}.gif', 'wb') as pic:
        pic.write(res.content)
    return res.content


def getInfo(code, guid, kword):
    url = f'http://cri.gz.gov.cn/Search/Result?validateCode={code}&guid={guid}&keywords={kword}'

    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # 'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'host': "cri.gz.gov.cn",
        'proxy-connection': "keep-alive",
        'referer': "http://cri.gz.gov.cn/Search/Result?validateCode=e6ecr&guid=C0606949BFA9F3052CF84D2747AAA0A2DD30B6FD13D94C08494A069249F5B85D&keywords=440126603901334",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    }
    res = sess.get(url, headers=headers)
    if kword not in res.text:
        print('again')
        return
    s = Selector(text=res.text)
    company_name = s.xpath('//*[contains(@class, "list-inline")]/li[last()]/text()').extract_first().replace('名称：',
                                                                                                             '').strip()
    p1 = s.xpath('//*[contains(@class, "inner-results")]/p[1]/text()').extract_first().strip()
    print(p1)
    p1l = p1.split('\xa0\xa0\xa0')
    p1l = [p.strip() for p in p1l if p.strip()]
    legal_person = p1l[0].replace('法定代表人：', '').strip()
    register_capital = p1l[1].replace('注册资本：', '').strip()
    establish_date = p1l[2].replace('成立日期：', '').strip()
    bussiness_duration = p1l[3].replace('营业期限：', '').strip()
    social_credit_code = s.xpath('//*[contains(@class, "inner-results")]/p[2]/text()').extract_first().replace(
        '社会信用代码：', '').strip()
    print(company_name)
    print(legal_person)
    print(register_capital)
    print(establish_date)
    print(bussiness_duration)
    print(social_credit_code)


def mainPic():
    guid = getGuid()
    getPic(guid)
    gif = f'./easy_img/{guid}.gif'
    png = f'./easy_img/{guid}.png'
    gif = Image.open(gif)
    gif.convert('RGB').save(png, 'png')
    gif.show()
    image = open(png, 'rb')
    code = baiduAPImain(image.read())
    getInfo(code, guid, '440126603901334')


if __name__ == '__main__':
    mainPic()
