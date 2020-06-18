import datetime
import os
import time
import xlwt
import xlrd
import re
from urllib.parse import urlencode, urlparse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

source_dir = os.path.join(os.getcwd(), 'source_files')
file_dir = os.path.join(os.getcwd(), 'files')
screenshot_dir = os.path.join(file_dir, 'screenshot')
excel_dir = os.path.join(file_dir, 'excel')
if not os.path.exists(file_dir):
    os.mkdir(file_dir)
if not os.path.exists(screenshot_dir):
    os.mkdir(screenshot_dir)
if not os.path.exists(excel_dir):
    os.mkdir(excel_dir)

querystring = {
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
url = "https://www.google.com/search"
comp = re.compile(r'imgurl=(.*?)&imgrefurl')


def write_xls(xls_lst, kw, st, time_now):
    """

    :param xls_lst: 要写入excel的list
    :param kw: 搜索关键字，用于构建文件名
    :param time_now: 当前时间，用于构建文件名
    :return:
    """
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")
    for i, l in enumerate(xls_lst):
        for j, col in enumerate(l):
            sheet.write(i, j, col)
    xls_file = os.path.join(excel_dir, '{}_{}_{}.xls'.format(kw, st, time_now))
    book.save(xls_file)


def open_url(kw, site):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=4096x2006')
    driver = webdriver.Chrome(options=chrome_options, executable_path=r'chromedriver.exe')
    query = querystring.copy()
    query.update({"q": "{} {}".format(kw, site)})
    real_url = url + '?' + urlencode(query)
    driver.get(real_url)
    driver.implicitly_wait(30)
    time.sleep(1)
    return driver


def screenshot(driver, kw, st, time_now):
    # # 滚动截屏
    print(' begin scroll screenshot~~~')
    shot_item_dir = os.path.join(screenshot_dir, '{}_{}_{}'.format(kw, st, time_now))
    os.mkdir(shot_item_dir)
    # 定义一个初始值
    print('     screenshot %d' % 1)
    driver.save_screenshot(os.path.join(shot_item_dir, '{}_{}_{}_{}.png'.format(1, kw, st, time_now)))
    temp_height = 0
    p = 2
    while 1:
        driver.execute_script("window.scrollBy(0,800)")
        driver.implicitly_wait(30)
        time.sleep(3)
        print('     screenshot %d' % p)
        driver.save_screenshot(os.path.join(shot_item_dir, '{}_{}_{}_{}.png'.format(p, kw, st, time_now)))
        # more = WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element_by_css_selector(".YstHxe"))
        try:
            more = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, "YstHxe")))
            time.sleep(1)
        except TimeoutException:
            more = None
        if more and more.get_attribute('style') != 'display: none;':
            more.click()
            driver.implicitly_wait(30)
        check_height = driver.execute_script(
            "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
        # 如果两者相等说明到底了
        if check_height == temp_height:
            break
        temp_height = check_height
        p += 1


def write_func(driver, kw, st, time_now):
    # 保存图片信息至xls
    print(' begin save pic-info into xls~~~')
    pic_as = driver.find_elements_by_xpath('//a[@class="VFACy kGQAp"]')
    xls_lst = list()
    for i, pic_a in enumerate(pic_as):
        pic_url = pic_a.get_attribute('href')
        url_tuple = urlparse(pic_url)
        pic_site = url_tuple[0] + '://' + url_tuple[1]
        pic_file = '{}_{}_{}_{}'.format(kw, st, time_now, i + 1)
        pic_file_m = '{}m'.format(pic_file)
        xls_lst.append([pic_url, pic_site, pic_file, pic_file_m])
    write_xls(xls_lst, kw, st, time_now)


def handle_one(kw, site):
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    driver = open_url(kw, site)
    driver.implicitly_wait(30)
    st = site.split(':')[-1]
    screenshot(driver, kw, st, time_now)
    write_func(driver, kw, st, time_now)
    driver.quit()


def main(keyfile_str, sitefile_str):
    keyfile = xlrd.open_workbook(keyfile_str)
    st = keyfile.sheet_by_index(0)
    lie = [str(st.cell_value(i, 0)) for i in range(st.nrows)]
    print(sitefile_str)
    sitefile = open(sitefile_str, 'r', encoding='utf-8')
    sites = sitefile.readlines()
    sitefile.close()
    for key in lie:
        for site in sites:
            key = key.strip()
            site = site.strip()
            print('searching: ', key, site)
            handle_one(key, site)
            print('\n\n')

    del keyfile


if __name__ == '__main__':
    keyfile_str = os.path.join(source_dir, 'Keyword seach_202005261744.xlsx')
    sitefile_str = os.path.join(source_dir, 'key.txt')
    main(keyfile_str, sitefile_str)
