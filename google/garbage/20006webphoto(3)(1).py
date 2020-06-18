from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import WebDriverException
import time
import pathlib
import os

##有一个ERROR LGO 20200523 NEW GAI MUST BE HTTP ,NOT WWW.
p = pathlib.Path('.')

csvs = [str(i) for i in p.glob("*.csv")]

time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())


def handle_csv(csv):
    out_dir = csv.split('.')[0]
    try:
        os.mkdir(out_dir)
    except:
        pass

    with open(csv, encoding='utf8', errors='replace') as fin:
        lines = fin.readlines()

    for line in lines:
        line = line.strip().split(',')
        if line[1].startswith("http"):
            url = line[1]
            print(url, end='\t', flush=True)
        elif line[1].startswith("wwww."):
            url = "http://" + line[1]
            print(url, end='\t', flush=True)
        else:
            print(line, "not an url, Error")
            continue
        try:
            driver.get(url)
            driver.get_screenshot_as_file(os.path.join(out_dir, f"{line[2]}_{time_now}.png"))
            print("OK")
        except WebDriverException:
            print("Error")
            with open(f"error_{time_now}.log", "a") as fout:
                fout.write(url + '\n')


option = FirefoxOptions()
option.headless = True
driver = Firefox(options=option)
driver.maximize_window()

for csv in csvs:
    handle_csv(csv)
