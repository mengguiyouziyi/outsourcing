# import execjs
# import requests
# import random
#
# session = requests.Session()
#
#
# class WenShu(object):
#     def __init__(self):
#         self.header_1 = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Cache-Control': 'max-age=0',
#             'Connection': 'keep-alive',
#             'Host': 'wenshu.court.gov.cn',
#             'Referer': 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
#         }
#         self.header_2 = {
#             'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#             'Accept-Encoding' : 'gzip, deflate',
#             'Accept-Language' : 'zh-CN,zh;q=0.9',
#             'Connection' : 'keep-alive',
#             'Cookie' : '',
#             'Host' : 'wenshu.court.gov.cn',
#             'Referer' : 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
#             'Upgrade-Insecure-Requests' : '1',
#             'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
#         }
#         self.header_3 = {
#             'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#             'Accept-Encoding' : 'gzip, deflate',
#             'Accept-Language' : 'zh-CN,zh;q=0.9',
#             'Connection' : 'keep-alive',
#             'Cookie' : '',
#             'Host' : 'wenshu.court.gov.cn',
#             'Referer' : 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6',
#             'Upgrade-Insecure-Requests' : '1',
#             'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
#         }
#
#     def get_wzws_1(self):
#         url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
#         response = session.get(url=url, headers=self.header_1)
#         wzws_1 = response.cookies.get_dict()
#         print(wzws_1)
#         return wzws_1['wzws_cid']
#
#     def get_wzws_2(self):
#         url = 'http://wenshu.court.gov.cn/WZWSREL0xpc3QvTGlzdD9zb3J0dHlwZT0xJmNvbmRpdGlvbnM9c2VhcmNoV29yZCsyK0FKTFgrKyVFNiVBMSU4OCVFNCVCQiVCNiVFNyVCMSVCQiVFNSU5RSU4QjolRTYlQjAlOTElRTQlQkElOEIlRTYlQTElODglRTQlQkIlQjY='
#         self.header_2['Cookie'] = 'wzws_cid={wzws_cid}'.format( wzws_cid=self.get_wzws_1())
#         print(self.header_2['Cookie'])
#         response = session.get(url=url, headers=self.header_2)
#         print(response.status_code)
#         wzws_2 = response.cookies.get_dict()
#         print(wzws_2)
#         return wzws_2['wzws_cid']
#
#     def get_vjkl5(self):
#         url = 'http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+2+AJLX++%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E6%B0%91%E4%BA%8B%E6%A1%88%E4%BB%B6'
#         self.header_3['Cookie'] = 'wzws_cid={wzws_cid}'.format(wzws_cid = self.get_wzws_2())
#         print(self.header_3['Cookie'])
#         response = session.get(url=url, headers=self.header_3)
#         vjkl5 = response.cookies.get_dict()
#         print(vjkl5)
#         # return vjkl5['vjkl5']
#
#
# if __name__ == '__main__':
#     wenshu = WenShu()
#     wenshu.get_vjkl5()
import requests

url = 'http://wenshu.court.gov.cn/list/list/?sorttype=1'
response = requests.get(url=url)