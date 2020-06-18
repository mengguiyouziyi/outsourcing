# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Request
from http.cookies import SimpleCookie


class WenSpider(scrapy.Spider):
    name = 'wen'
    # vjkl5
    custom_settings = {
        # 'DEFAULT_REQUEST_HEADERS': {
        # },
        'LOG_LEVEL': 'DEBUG',
        'DOWNLOAD_DELAY': 1,
        # 'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'DOWNLOADER_MIDDLEWARES': {
            # 'scrapyProject.middlewares.RotateUserAgentMiddleware': 3,
        },
        'ITEM_PIPELINES': {
            # 'scrapyProject.pipelines.MysqlPipeline': 999,
            # 'scrapyProject.pipelines.DuplicatesPipeline': 111,
        },
    }

    def __init__(self):
        self.header1 = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'wenshu.court.gov.cn',
            # 'cookie': "Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1556591502; _gscu_2116842793=01577230j6u6bc20; _gscbrs_2116842793=1; ASP.NET_SessionId=mvp3hbfmrkty4xupdqd03zh2; vjkl5=5eb095ff206c75010518847584cba01b12c75e4a; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1556592266; _gscs_2116842793=56591502bwyxid74|pv:6; wzws_cid=335ee2c0e27fc717e999609f0495295295a762bec3f2d48a76e21af4e2a82e6c638f6075d417f5967094ebe8987a0b35acb8ce05eaa0a2de45b996d42e3ea9405319bfec1e20306f9f0f6160a324848875e4b914dced15fc4cdda64e0446b195",
            'Referer': 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            # 'upgrade-insecure-requests': "1",
            # 'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            # 'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        }


    def start_requests(self):
        url = 'http://wenshu.court.gov.cn/WZWSRELw==?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDc4NDg1NTI='
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
            'connection': "keep-alive",
            # 'cookie': "Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1556591502; _gscu_2116842793=01577230j6u6bc20; _gscbrs_2116842793=1; ASP.NET_SessionId=mvp3hbfmrkty4xupdqd03zh2; vjkl5=5eb095ff206c75010518847584cba01b12c75e4a; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1556592266; _gscs_2116842793=56591502bwyxid74|pv:6; wzws_cid=335ee2c0e27fc717e999609f0495295295a762bec3f2d48a76e21af4e2a82e6c638f6075d417f5967094ebe8987a0b35acb8ce05eaa0a2de45b996d42e3ea9405319bfec1e20306f9f0f6160a324848875e4b914dced15fc4cdda64e0446b195",
            'host': "wenshu.court.gov.cn",
            'referer': "http://wenshu.court.gov.cn/",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        }
        cookie = "Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1556591502; _gscu_2116842793=01577230j6u6bc20; _gscbrs_2116842793=1; ASP.NET_SessionId=mvp3hbfmrkty4xupdqd03zh2; vjkl5=5eb095ff206c75010518847584cba01b12c75e4a; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1556592266; _gscs_2116842793=56591502bwyxid74|pv:6; wzws_cid=335ee2c0e27fc717e999609f0495295295a762bec3f2d48a76e21af4e2a82e6c638f6075d417f5967094ebe8987a0b35acb8ce05eaa0a2de45b996d42e3ea9405319bfec1e20306f9f0f6160a324848875e4b914dced15fc4cdda64e0446b195"
        cookies = {i.key: i.value for i in SimpleCookie(cookie).values()}
        yield scrapy.Request(url=url, headers=headers)

    def parse(self, response):
        print(response.headers['Set-Cookie'])
        print(response.request.headers['Cookie'])
        url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
        headers = {
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse1)

    def parse1(self, response):
        print(response.headers['Set-Cookie'])
        print(response.request.headers['Cookie'])

        url = 'http://wenshu.court.gov.cn/WZWSREL0xpc3QvTGlzdD9zb3J0dHlwZT0xJmNvbmRpdGlvbnM9c2VhcmNoV29yZCsyK0FKTFgrKyVFNiVBMSU4OCVFNCVCQiVCNiVFNyVCMSVCQiVFNSU5RSU4QjolRTYlQjAlOTElRTQlQkElOEIlRTYlQTElODglRTQlQkIlQjY=?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDc4NTY5NzI='
        # Cookie = response.headers.getlist('Set-Cookie')[0].decode('utf-8')
        # self.header1['Cookie'] = Cookie
        yield scrapy.Request(url=url, headers=self.header1, callback=self.first)

    def first(self, response):
        print(response.headers['Set-Cookie'])
        print(response.request.headers['Cookie'])
        url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
        # Cookie = response.headers.getlist('Set-Cookie')[0].decode('utf-8')
        # self.header1['Cookie'] = Cookie
        yield scrapy.Request(url=url, headers=self.header1, callback=self.second, dont_filter=True)

    def second(self, response):
        print(response.headers['Set-Cookie'])
        print(response.request.headers['Cookie'])
        # Cookie = response.headers.getlist('Set-Cookie')[0].decode('utf-8')
        # print(Cookie)
