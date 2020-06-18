import os
import json
import time
import requests
# from traceback import print_exc

sess = requests.session()

url = 'http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E9%97%AE%E8%AF%A2%E5%87%BD&sdate={start}' \
      '&edate={end}&isfulltext=false&sortName=nothing&sortType=desc&pageNum={pn}'

bdir = r'D:\My Package\My project\documents\cninfo'  # bdir should be changed to your base_directory
dps = [
    ['2000-01-01', '2016-01-01', 203],
    ['2016-01-01', '2016-12-31', 468],
    ['2017-01-01', '2017-12-31', 582],
    ['2018-01-01', '2018-11-30', 575],
    ['2018-12-01', '2019-07-23', 466],
]

# http://static.cninfo.com.cn/finalpage/2019-07-12/1206441819.PDF
for dp in dps:
    for p in range(1, dp[2] + 1):
        try:
            print(url.format(start=dp[0], end=dp[1], pn=p))
            res = sess.get(url.format(start=dp[0], end=dp[1], pn=p)).json()
            fileName = dp[0] + '_' + dp[1] + '_' + str(dp[2]) + '_' + str(p) + '.json'
            with open(os.path.join(bdir, fileName), 'w', encoding='utf-8') as j:
                json.dump(res, j, ensure_ascii=False)
        except:
            # print_exc()
            continue
        time.sleep(0.5)


def formatUrl(url):
    """
        json文件中的url是相对uri，需要在前面加上域名
    :param url:
    :return:
    """
    return 'http://static.cninfo.com.cn/' + url


def formatDate(timeStamp):
    """
        json文件中的时间戳是（*1000）放大1000倍的时间戳整数，需要除以1000，再变成需要的时间格式
    :param timeStamp:
    :return:
    """
    import datetime

    # timeStamp = 1440691200000
    timeArray = datetime.datetime.utcfromtimestamp(timeStamp / 1000)
    formatTime = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    print(formatTime)
    return formatTime
