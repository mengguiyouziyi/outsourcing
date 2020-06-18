import requests
from pprint import pprint

ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
resp_headers = {
    'accept': "application/json, text/plain, */*",
    'user-agent': ua,
    'content-type': "application/json",
}
login_headers = {
    'origin': "https://www.tradesparq.com",
    'upgrade-insecure-requests': "1",
    'content-type': "application/x-www-form-urlencoded",
    'user-agent': ua,
    'sec-fetch-user': "?1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
url = "https://api4.tradesparq.com/customs/buyer/searching"

def login():
    sess = requests.session()
    url = "https://user.tradesparq.com/public/user/do_login"
    login_payload = "email=waimao829%40163.com&password=waimao2019&rememberMe=1"
    sess.request("POST", url, data=login_payload, headers=login_headers)
    return sess


def getresp(sess):
    payload = '{"product":"%(kw)s","pageIndex":%(page)d,"pageSize":100}'
    obj = sess.request("POST", url, data=payload % {'kw': 'brush machines', 'page': 5}, headers=resp_headers,
                            timeout=20).json()
    pprint(obj['data']['data'][85])


if __name__ == '__main__':
    sess = login()
    getresp(sess)
