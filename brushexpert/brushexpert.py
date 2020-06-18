# -*- coding: UTF-8 -*-
# ***********************************************
# **  file：     brushexpert.py
# **  purpose：  brushexpert spider
# **
# **  author:    mengguiyouziyi
# **  date:      2018/12/05
# ***********************************************

import time
import requests
import pandas as pd
import os
import sys
from selenium import webdriver
from scrapy.selector import Selector
from urllib.parse import urljoin
from collections import defaultdict
from traceback import print_exc
from random import choice
from multiprocessing import Process


def writePng(url, png_path):
    try:
        fox = webdriver.Firefox(executable_path=r'..\geckodriver.exe')
    except KeyboardInterrupt as e:
        print('Keyboard Interrupt ~~~~')
        exit()
    except:
        fox = webdriver.Firefox()
    fox.set_page_load_timeout(360)
    try:
        fox.get(url)
        fox.maximize_window()
        element = fox.find_element_by_id('main')
        png = element.screenshot_as_png
        png_file = f'{png_path}.png'
        with open(png_file, 'wb') as out:
            out.write(png)
    except KeyboardInterrupt as e:
        print('Keyboard Interrupt ~~~~')
        exit()
    except:
        # print_exc()
        print('Firefox timeout, retry!')
        return 'fail'
    finally:
        fox.quit()


# USER_AGENT_CHOICES = [
#     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/62.0',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
#     'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
# ]
# s = requests.session()
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'connection': "close",
    'cookie': "ASP.NET_SessionId=1uamxq2aub15xylkvei4o2yj; ARRAffinity=515e4622af4613575903133cdd6545693e7207af9c7fc84c5b1ed6cd7844cdf9; _ga=GA1.2.808518053.1543831615; _gid=GA1.2.1080940497.1543831615; _gat=1",
    'host': "www.brushexpert.com",
    'referer': "https://www.brushexpert.com/directory/finished_products/page/2/",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
}
bpath = os.path.join(os.getcwd(), 'file')
if not os.path.exists(bpath):
    os.makedirs(bpath)


# bpath = r'D:\My Package\My project\documents\outword'

def get_res_try(url):
    try:
        res = requests.get(url, headers=headers, timeout=30)
        return res
    except Exception as e:
        # print(repr(e))
        return


def get_res_loop(url):
    what = get_res_try(url)
    n = 0
    while not what:
        n += 1
        what = get_res_try(url)
        print('Get website failed, retry %d times!' % n)
    return what


# todo distribute
def linePng(num):
    count = 0
    cdict = defaultdict(lambda: 0)
    for page in range(1, 53):
        print('*' * 30)
        print('*' * 10, page, 'page', '*' * 10)
        print('*' * 30)
        page_url = f'https://www.brushexpert.com/directory/finished_products/page/{page}/'
        res = get_res_loop(page_url)
        sel = Selector(text=res.text)
        for div in sel.xpath('//*[starts-with(@class, "listed")]'):
            count += 1
            print('-' * 5, count, '-' * 5)
            if count < num:
                continue
            item = defaultdict(lambda: None)
            item['url'] = urljoin('https://www.brushexpert.com', div.xpath('./div[1]/a/@href').extract_first())
            item['name'] = div.xpath('./div[1]/a/text()').extract_first()
            country = div.xpath('./div[2]/a/text()').extract_first()
            item['country'] = country if country else 'None'

            cdict[item['country']] = cdict[item['country']] + 1
            item_base_path = item['country'] + str(cdict[item['country']])
            item_png = os.path.join(bpath, item_base_path)
            result_str = writePng(item['url'], item_png)
            while result_str == 'fail':
                print('write png fail, again!')
                result_str = writePng(item['url'], item_png)
            print('write png success!')


def lineCsv(num):
    count = 0
    list_csv = os.path.join(bpath, 'list.csv')
    cdict = defaultdict(lambda: 0)
    for page in range(1, 53):
        print('*' * 30)
        print('*' * 10, page, 'page', '*' * 10)
        print('*' * 30)
        page_url = f'https://www.brushexpert.com/directory/finished_products/page/{page}/'
        res = get_res_loop(page_url)
        sel = Selector(text=res.text)
        for div in sel.xpath('//*[starts-with(@class, "listed")]'):
            count += 1
            print('-' * 5, count, '-' * 5)
            if count < num:
                continue
            item = defaultdict(lambda: None)
            item['url'] = urljoin('https://www.brushexpert.com', div.xpath('./div[1]/a/@href').extract_first())
            print(item['url'])
            item['name'] = div.xpath('./div[1]/a/text()').extract_first()
            country = div.xpath('./div[2]/a/text()').extract_first()
            item['country'] = country if country else 'None'

            cdict[item['country']] = cdict[item['country']] + 1
            item_base_path = item['country'] + str(cdict[item['country']])

            item['host'] = div.xpath('./div[3]/a[1]/@href').extract_first()
            email = div.xpath('./div[3]/a[2]/@href').extract_first()
            item['email'] = email.replace('mailto:', '') if email else None

            # headers['user-agent'] = choice(USER_AGENT_CHOICES)
            dres = get_res_loop(item['url'])
            # time.sleep(0.1)
            dsel = Selector(text=dres.text)
            info = dsel.xpath('//*[@id="directoryListing"]')
            addrs = info.xpath('./div[not(@*)]/text()').extract()
            item['addr'] = ' '.join([x.strip() for x in addrs if x.strip()]).replace(',', '')
            tel_fax = info.xpath('./a[@class="geoLink"]/following-sibling::*[1]/text()').extract()
            tel_fax = [x.strip() for x in tel_fax if x.strip()]
            if len(tel_fax) == 2:
                item['tel'] = tel_fax[0]
                item['fax'] = tel_fax[1]
            elif len(tel_fax) == 1:
                item['tel'] = tel_fax[0]
            # print(item.items())
            del item['url'], item['host']

            item_csv = os.path.join(bpath, item_base_path + '.csv')
            data = pd.DataFrame(item, index=[0])
            data.to_csv(item_csv, sep='\n', header=False, index=False)
            print('write single csv success!')
            data.to_csv(list_csv, mode='a', header=False, index=False)
            print('write list csv success!')


def mainParameter():
    """
    命令式，直接输入csv或png作为参数
        > python brushexpert.py csv
        > python brushexpert.py png
    :return:
    """
    if len(sys.argv) != 3:
        print('Please input the like this form: < python brushexpert.py csv 120 >')
        exit(1)
    if sys.argv[1] == 'csv':
        lineCsv(int(sys.argv[2]))
    else:
        linePng(int(sys.argv[2]))


def mainInteractive():
    """
    交互式
        in  > python brushexpert.py
        out > Please input the spider<csv png>: csv
        in  > python brushexpert.py
        out > Please input the spider<csv png>: png
    :return:
    """
    into = input('Please input the spider<csv png>: ')
    num = int(input('Please input the num you want to start: '))
    if into == 'csv':
        lineCsv(num)
    else:
        linePng(num)


if __name__ == '__main__':
    try:
        mainInteractive()
    except KeyboardInterrupt as e:
        print('Keyboard Interrupt ~~~~')
        exit()
    # mainParameter()
