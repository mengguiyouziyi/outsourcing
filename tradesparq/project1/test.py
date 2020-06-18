import base64
import json
import requests


def getImg(pic):
    f = open(r'.\pics\{}'.format(pic), 'rb')
    img_byte = base64.b64encode(f.read())
    img_str = img_byte.decode('ascii')
    data = {'img': img_str}
    json_mod = json.dumps(data)
    response_code = requests.post(url='http://127.0.0.1:8007/zqsx', data=json_mod)
    img = response_code.text.replace('_', '')
    print(img)
    return img


if __name__ == '__main__':
    img = getImg(pic='captcha.jpg')
