# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
import random #随机选择
from .settings import rand_choi_pool
from .useragent import agents #导入前面的
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #UserAegent中间件

class UserAgentmiddleware(UserAgentMiddleware):  # UA中间件
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent


class ProxyMiddleware(object):  # 代理中间件
    '''
    设置Proxy
    '''

    def __init__(self, ip):
        self.ip = ip

    @classmethod
    def from_crawler(cls, crawler):
        return cls(ip=crawler.settings.get('PROXIES'))
        # return cls(ip=PROXIES)

    def process_request(self, request, spider):
        ip = random.choice(self.ip)
        # print('当前使用的ip是:', ip)
        if request.url == 'http://127.0.0.1:8008/zqsx':
            request.meta['proxy'] = ''
            # print(request.url, '当前使用的ip是:', request.meta['proxy'])
        else:
            request.meta['proxy'] = ip
            # print(request.url, '当前使用的ip是:', ip)
            
            
class ProxyMiddlewarePool(object):  # 代理中间件
    '''
    设置Proxy
    '''
    def process_request(self, request, spider):
        ip = rand_choi_pool()
        # print('当前使用的ip是:', ip)
        if request.url == 'http://127.0.0.1:8008/zqsx':
            request.meta['proxy'] = ''
            # print(request.url, '当前使用的ip是:', request.meta['proxy'])
        else:
            request.meta['proxy'] = ip
            # print(request.url, '当前使用的ip是:', ip)