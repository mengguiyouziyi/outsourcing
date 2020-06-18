import datetime
import time
import os
import xlwt
import xlrd
import re
import urllib.request as ur
from urllib.parse import urlencode, urlparse
from selenium import webdriver

opener = ur.build_opener()
opener.addheaders = [
    ('User-Agent',
     'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')
]
ur.install_opener(opener)

file_dir = os.path.join(os.getcwd(), 'files')
screenshot_dir = os.path.join(file_dir, 'screenshot')
pic_dir = os.path.join(file_dir, 'pics')
excel_dir = os.path.join(file_dir, 'excel')
if not os.path.exists(file_dir):
    os.mkdir(file_dir)
if not os.path.exists(screenshot_dir):
    os.mkdir(screenshot_dir)
if not os.path.exists(pic_dir):
    os.mkdir(pic_dir)
if not os.path.exists(excel_dir):
    os.mkdir(excel_dir)

url = "https://www.google.com/search"
comp = re.compile(r'imgurl=(.*?)&imgrefurl')
slp = 5


def cbk(a, b, c):
    '''回调函数
    @a: 已经下载的数据块
    @b: 数据块的大小
    @c: 远程文件的大小
    '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def down(url, file):
    ur.urlretrieve(url, file, cbk)


def write_xls(xls_lst, kw, time_now, excel_dir):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")
    for i, l in enumerate(xls_lst):
        for j, col in enumerate(l):
            sheet.write(i, j, col)
    xls_file = os.path.join(excel_dir, '{} {}.xls'.format(kw, time_now))
    book.save(xls_file)


def main(kw, site):
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    querystring1 = {
        "q": "{} {}".format(kw, site),
        "tbm": "isch",
        "ved": "2ahUKEwjc-fTj5uLpAhUMbJQKHXjBBQwQ2-cCegQIABAA",
        "oq": "Wiring devices site:sa",
        "gs_lcp": "CgNpbWcQDFAAWABgguMHaABwAHgAgAEAiAEAkgEAmAEAqgELZ3dzLXdpei1pbWc",
        "sclient": "img",
        "ei": "4hnWXtyAMozY0QT4gpdg",
        "bih": "936",
        "biw": "1920",
        "rlz": "1C1GCEU_zh-CNCN864HK864"
    }
    real_url = url + '?' + urlencode(querystring1)
    driver.get(real_url)
    driver.maximize_window()
    time.sleep(slp)
    try:
        # # 滚动截屏
        print('begin scroll screenshot~~~')
        shot_item_dir = os.path.join(screenshot_dir, '{} {}'.format(kw, time_now))
        os.mkdir(shot_item_dir)
        driver.save_screenshot(os.path.join(shot_item_dir, '{}_{} {}.png'.format(1, kw, time_now)))
        # 定义一个初始值
        temp_height = 0
        p = 2
        while 1:
            driver.execute_script("window.scrollBy(0,800)")
            time.sleep(slp)
            driver.save_screenshot(os.path.join(shot_item_dir, '{}_{} {}.png'.format(p, kw, time_now)))
            try:
                more = driver.find_element_by_xpath('//div[@class="YstHxe"]')
            except Exception as e:
                print(e)
                return
            if more.get_attribute('style') != 'display: none;':
                more.click()
                time.sleep(slp)
            try:
                check_height = driver.execute_script(
                    "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            except Exception as e:
                print(e)
                try:
                    check_height = driver.execute_script(
                        "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
                except Exception as e:
                    print(e)
                    return
            # 如果两者相等说明到底了
            if check_height == temp_height:
                break
            temp_height = check_height
            p += 1

        # 保存图片信息至xls
        print(' begin save pic-info into xls~~~')
        pic_as = driver.find_elements_by_xpath('//a[@class="VFACy kGQAp"]')
        xls_lst = list()
        for i, pic_a in enumerate(pic_as):
            try:
                pic_url = pic_a.get_attribute('href')
                # pic_site = pic_a.find_element_by_class_name('fxgdke').text
                url_tuple = urlparse(pic_url)
                pic_site = url_tuple[0] + '://' + url_tuple[1]
                # pic_site = pic_site.replace(' · 有货', '').replace(' · 缺货', '') if pic_site else ''
                pic_file = '{} {}_{}'.format(kw, time_now, i + 1)
                pic_file_m = '{} {}_{}m'.format(kw, time_now, i + 1)
                xls_lst.append([pic_url, pic_site, pic_file, pic_file_m])
            except Exception as e:
                print(e)
                continue
        write_xls(xls_lst, kw, time_now, excel_dir)

        """
        # 下载图片
        down_as = driver.find_elements_by_xpath('//a[@class="wXeWr islib nfEiy mM5pbd"]')
        down_urls = list()
        down_num = 1
        print('begin append url into list~~~')
        for down_a in down_as:
            print(down_num)
            try:
                # 点击两次是为了执行点击事件，生成完图片url后，将右侧弹窗消去
                driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[{}]'.format(down_num)).click()
                time.sleep(slp)
                driver.find_element_by_xpath('//*[@class="IA8gLe"]').click()
                long = down_a.get_attribute('href')
                if not long:
                    driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[{}]'.format(down_num)).click()
                    time.sleep(slp)
                    driver.find_element_by_xpath('//*[@class="IA8gLe"]').click()
                    time.sleep(slp)
                    long = down_a.get_attribute('href')
                if not long:
                    continue
                long = unquote(long)
                jpg_url = comp.findall(long)
                if not jpg_url:
                    continue
                jpg_url = jpg_url[0]
                down_urls.append(jpg_url)
            except Exception as e:
                print(e)
                continue
            down_num += 1
        pic_item_dir = os.path.join(pic_dir, '{} {}'.format(kw, time_now))
        os.mkdir(pic_item_dir)
        print('begin downloading~~~')
        for i, (down_url, xls_line) in enumerate(zip(down_urls, xls_lst)):
            if 'jpg' in down_url:
                file = os.path.join(pic_item_dir, xls_line[2] + '.jpg')
            elif 'png' in down_url:
                file = os.path.join(pic_item_dir, xls_line[2] + '.png')
            else:
                file = os.path.join(pic_item_dir, xls_line[2] + '.{}'.format(down_url[-3:]))
            print(i + 1, down_url, '~~~', file)
            try:
                down(down_url, file)
            except Exception as e:
                print(e)
                continue
        """
    except Exception as e:
        print(e)
        return
    else:
        return True
    finally:
        driver.quit()


if __name__ == '__main__':
    keyfile_str = 'Keyword seach_202005261744.xlsx'
    keyfile = xlrd.open_workbook(keyfile_str)
    st = keyfile.sheet_by_index(0)
    lie = [str(st.cell_value(i, 0)) for i in range(st.nrows)]
    sitefile = open('key.txt', 'r', encoding='utf-8')
    sites = sitefile.readlines()
    for key in lie:
        for site in sites:
            key = key.strip()
            site = site.strip()
            print('searching: ', key, site)
            # main(key, site)
            retry = 1
            myresult = main(key, site)
            while not myresult:
                print(' retry {} times'.format(retry))
                if retry > 2:
                    print(" please check the program's error!")
                    break
                myresult = main(key, site)
                retry += 1

    sitefile.close()
    del keyfile
