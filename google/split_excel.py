import os
import time
import xlwt
import xlrd
import datetime
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.chrome.options import Options

file_dir = os.path.join(os.getcwd(), 'files')
screenshot_site_dir = os.path.join(file_dir, 'screenshot_site')
excel_dir = os.path.join(file_dir, 'excel')
off_dir = os.path.join(file_dir, 'off')
if not os.path.exists(file_dir):
    os.mkdir(file_dir)
if not os.path.exists(screenshot_site_dir):
    os.mkdir(screenshot_site_dir)
if not os.path.exists(off_dir):
    os.mkdir(off_dir)
if not os.path.exists(excel_dir):
    os.mkdir(excel_dir)


def screenshot(driver, url, pic_str, shot_item_dir):
    try:
        print(' request and screenshot %s' % url)
        driver.get(url)
        driver.implicitly_wait(30)
        time.sleep(1)
        driver.save_screenshot(os.path.join(shot_item_dir, pic_str + '.png'))
    except UnexpectedAlertPresentException as e:
        print(e)
        driver.save_screenshot(os.path.join(shot_item_dir, pic_str + '.png'))
    except TimeoutException as e:
        print(e)
        try:
            driver.save_screenshot(os.path.join(shot_item_dir, pic_str + '.png'))
        except Exception as e:
            print(e)
            return
    except Exception as e:
        print(e)
        return


def write_xls(xls_lst, kw, time_now):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")
    for i, l in enumerate(xls_lst):
        for j, col in enumerate(l):
            sheet.write(i, j, col)
    xls_file = os.path.join(off_dir, '{}_{}.xls'.format(kw, time_now))
    book.save(xls_file)


def read_xls(file_str):
    file = xlrd.open_workbook(os.path.join(excel_dir, file_str))
    st = file.sheet_by_index(0)
    lines = [st.row_values(i) for i in range(st.nrows)]
    return lines


def deduplicate(driver, lines, shot_item_dir):
    xls_lst = list()
    dedup = set()
    for i, line in enumerate(lines):
        if line[1] in dedup:
            continue
        else:
            xls_lst.append(line)
            dedup.add(line[1])
            print(' handle %d line' % (i + 1))
            screenshot(driver, line[1], line[3], shot_item_dir)
    return xls_lst


def main(driver, file_str):
    kw = '_'.join(file_str.split('_')[:-1])
    time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    shot_item_dir = os.path.join(screenshot_site_dir, '{}_{}'.format(kw, time_now))
    os.mkdir(shot_item_dir)
    lines = read_xls(file_str)
    xls_lst = deduplicate(driver, lines, shot_item_dir)
    write_xls(xls_lst, kw, time_now)


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--window-size=4096x2006')
    driver = webdriver.Chrome(options=chrome_options, executable_path=r'chromedriver.exe')
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)  # 这两种设置都进行才有效
    driver.maximize_window()
    for file_str in os.listdir(excel_dir):
        print('reading %s' % file_str)
        main(driver, file_str)
    driver.quit()
