import requests

s = requests.session()


def getcookies():
    url = 'http://wenshu.court.gov.cn/WZWSRELw==?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDc4NDg1NTI='
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
        'connection': "keep-alive",
        'cookie': "Hm_lvt_d2caefee2de09b8a6ea438d74fd98db2=1556591502; _gscu_2116842793=01577230j6u6bc20; _gscbrs_2116842793=1; ASP.NET_SessionId=mvp3hbfmrkty4xupdqd03zh2; vjkl5=5eb095ff206c75010518847584cba01b12c75e4a; Hm_lpvt_d2caefee2de09b8a6ea438d74fd98db2=1556592266; _gscs_2116842793=56591502bwyxid74|pv:6; wzws_cid=335ee2c0e27fc717e999609f0495295295a762bec3f2d48a76e21af4e2a82e6c638f6075d417f5967094ebe8987a0b35acb8ce05eaa0a2de45b996d42e3ea9405319bfec1e20306f9f0f6160a324848875e4b914dced15fc4cdda64e0446b195",
        'host': "wenshu.court.gov.cn",
        'referer': "http://wenshu.court.gov.cn/",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    }
    res = s.get(url, headers=headers)
    print(s.cookies.items())
    print(res.cookies.items())


def get_cookies(conditions):
    url = "http://wenshu.court.gov.cn/List/List"
    querystring = {"sorttype": "1", "conditions": conditions}
    headers = {
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    }
    print(s.cookies.items())
    res = s.request("GET", url, headers=headers, params=querystring)
    print(s.cookies.items())
    print(res.cookies.items())
    print(res.request.headers['Cookie'])
    return s.cookies.get('vjkl5')


getcookies()
get_cookies('searchWord 1 AJLX  案件类型:刑事案件')
