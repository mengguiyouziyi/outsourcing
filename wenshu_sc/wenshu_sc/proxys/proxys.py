PROXIES=[
    'http://106.12.199.35:8089',
    'http://106.12.199.151:8089',
    'http://106.12.199.161:8089',
    'http://106.12.128.78:8089',
    'http://106.12.31.86:8089',
    'http://106.12.83.54:8089',
    'http://106.12.133.155:8089',
    'http://106.12.128.176:8089',
    'http://106.12.89.102:8089',
    'http://106.12.199.170:8089',
    'http://106.12.128.179:8089',
    'http://106.12.133.218:8089',
    'http://106.12.199.214:8089',
    'http://106.12.134.175:8089',
    'http://106.12.85.211:8089',
    'http://106.12.133.224:8089',
    'http://106.12.101.33:8089',
    'http://106.12.210.101:8089',
    'http://106.12.202.115:8089',
    'http://106.12.101.239:8089',
    'http://106.12.89.250:8089',
    'http://106.12.90.57:8089',
    'http://182.61.27.83:8089',
    'http://106.12.204.18:8089',
    'http://106.12.90.3:8089',
    'http://182.61.49.100:8089',
    'http://106.12.204.65:8089',
    'http://106.12.199.181:8089',
    'http://106.12.8.69:8089',
    'http://106.12.199.193:8089',
    'http://106.12.128.100:8089',
    'http://106.12.128.202:8089'
]


import requests
import json
import random

def rand_choi():
    proxy = random.choice(PROXIES)
    proxies = {
        'http': 'http://' + proxy.replace('http://', ''),
        'https': 'https://' + proxy.replace('http://', ''),
    }
    return proxies

def rand_choi_pool():
    url = 'http://117.50.2.184:88/ippool'
    response = requests.get(url=url)
    ippool = json.loads(response.text)['ippool']
    proxy_demo = random.choice(ippool)
    proxies = {
        'http': proxy_demo,
        'htttps': proxy_demo.replace('http', 'https'),
    }
    # print(proxies)
    return proxy_demo