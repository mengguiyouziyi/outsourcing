from selenium import webdriver
from PIL import Image
import datetime

time_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def getPic():
    # fox = webdriver.Firefox(executable_path=r'..\geckodriver.exe')
    fox = webdriver.Firefox()
    fox.get('https://www.smm.cn/')
    fox.maximize_window()
    # now that we have the preliminary stuff out of the way time to get that image :D
    element = fox.find_elements_by_class_name('content-left-first-pirce')  # find part of the page you want image of

    a = element[0].screenshot_as_png
    b = element[1].screenshot_as_png

    apic = f'A{time_now}.png'
    bpic = f'B{time_now}.png'
    with open(apic, 'wb') as out1, open(bpic, 'wb') as out2:
        out1.write(a)
        out2.write(b)

    fox.quit()
    return apic, bpic


def montagePic(apic, bpic):
    """470 684 470 538"""
    a = Image.open(apic)
    b = Image.open(bpic)
    aw, ah = a.size
    bw, bh = b.size
    toImage = Image.new("RGBA", (aw, ah + bh))
    toImage.paste(a, (0, 0))
    toImage.paste(b, (0, ah))
    print('canvas size: ', toImage.size)
    toImage.save(f'{time_now}.png')


if __name__ == '__main__':
    apic, bpic = getPic()
    montagePic(apic, bpic)
