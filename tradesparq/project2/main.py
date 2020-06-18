import datetime
import os
import time
import xlwt
import random
import requests
from math import ceil
from ua import uas

file_dir_str = 'files'
root_dir = os.getcwd()
file_dir = os.path.join(root_dir, file_dir_str)
if not os.path.exists(file_dir):
    os.mkdir(file_dir)


def _result(result):
    return result is None


url = "https://api4.tradesparq.com/customs/buyer/searching"
login_headers = {
    'origin': "https://www.tradesparq.com",
    'upgrade-insecure-requests': "1",
    'content-type': "application/x-www-form-urlencoded",
    'user-agent': random.choice(uas),
    'sec-fetch-user': "?1",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}
resp_headers = {
    'accept': "application/json, text/plain, */*",
    'user-agent': random.choice(uas),
    'content-type': "application/json",
}
payload = '{"product":"%(kw)s","pageIndex":%(page)d,"pageSize":100}'
login_url = "https://user.tradesparq.com/public/user/do_login"
login_payload = "email=waimao829%40163.com&password=waimao2019&rememberMe=1"


def login():
    sess = requests.session()
    sess.request("POST", login_url, data=login_payload, headers=login_headers)
    return sess


def get_resp(sess, kw, p):
    """
    获取请求响应
    :param kw:
    :param p:
    :return:
    """
    try:
        response = sess.request("POST", url, data=payload % {'kw': kw, 'page': p}, headers=resp_headers, timeout=20)
        if response.status_code != 200:
            print(' response is not 200, response.status_code is %d' % response.status_code)
            return
        obj = response.json()
    except Exception as e:
        print(e)
        return
    return obj


def get_data(sess, kw, p=1):
    """
    翻页，从返回的json中提取data，并加入datas列表（所有页码的）
    data格式 data=[{"countryEn":"United States","country":"美国", ...}, ...]
    :param kw:
    :return:
    """
    if p == 1:
        print(' page %d' % 1)
        obj = get_resp(sess, kw, 1)
        if not obj:
            print(' first page no obj')
            return
        data_dict = obj.get('data', {})
        data = data_dict.get('data', [])
        if not data_dict or not data:
            print(' first page not have data_dict or data')
            return
        total = data_dict.get('total', 0)
        pages = int(ceil(total / 100))
        return data, pages
    else:
        print(' page %d' % p)
        obj = get_resp(sess, kw, p)
        if not obj:
            print(' other page no obj, next page')
            return
        data_dict = obj.get('data', {})
        data = data_dict.get('data', [])
        if not data_dict or not data:
            print(' other page not have data_dict or data, next page')
            return
        return data


def write_file(datas, file_str):
    lst = []
    lst.append('公司名字,国别(中文),国别(英文),联系人,邮箱,电话,地址,网址,传真'.split(','))
    for data in datas:
        email = data.get('email')
        line = [
            data.get('name'),
            data.get('country'),
            data.get('countryEn'),
            data.get('contact'),
            ' / '.join(email) if email else None,
            data.get('tel'),
            data.get('address'),
            data.get('website'),
            data.get('fax')
        ]
        lst.append(line)

    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")
    for i, l in enumerate(lst):
        for j, col in enumerate(l):
            sheet.write(i, j, col)
    book.save(os.path.join(file_dir, file_str))


def main(file='keyword.txt'):
    key_file = open(file, 'r', encoding='utf-8')
    for kw in key_file:
        kw = kw.strip()
        print('searching: ', kw)
        dt_format = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        start = time.time()

        sess = login()
        data_first, pages = get_data(sess, kw)
        first_data_retry = 1
        while not data_first:
            time.sleep(random.randint(5, 10))
            if first_data_retry > 3:
                break
            sess = login()
            data_first, pages = get_data(sess, kw)
            first_data_retry += 1
        if not data_first:
            print(' get no data_first, skip and continue!')
            time.sleep(random.randint(5, 10))
            continue
        data_lst = list()
        data_lst.extend(data_first)
        if pages > 3:
            endpage = 3
        else:
            endpage = pages
        for p in range(2, endpage + 1):
            time.sleep(random.randint(5, 10))
            data_other = get_data(sess, kw, p)
            other_data_retry = 1
            while not data_other:
                time.sleep(random.randint(5, 10))
                if other_data_retry > 3:
                    break
                sess = login()
                data_other = get_data(sess, kw, p)
                other_data_retry += 1
            if not data_other:
                time.sleep(random.randint(5, 10))
                print(' get no data_other, skip and continue!')
                continue
            data_lst.extend(data_other)

        end = time.time()

        file_str = '{kw}_{dt_format}_{row_num}_{use_time}.xls'.format(kw=kw, dt_format=dt_format, row_num=len(data_lst),
                                                                      use_time=int(end - start))
        write_file(datas=data_lst, file_str=file_str)
        time.sleep(random.randint(10, 20))
        print()
    key_file.close()


if __name__ == '__main__':
    main()
