import js2py
import execjs
import requests

import sys
import os

sys.path.append(os.path.dirname(__file__))

cpath = os.getcwd()


def get(vjkl5):
	# vjkl5 = 'eb58acddb95fff16b67014a18656504888345f9b'
	# 生成加密字符串vl5x和guid

	with open(os.path.join(cpath, 'guid文件.js'), 'r') as f:
		js_guid = f.read()
	with open('./第一个.js', 'r') as f:
		js_content = f.read()
	with open('./md5.js', 'r') as f:
		js_md5 = f.read()
	with open('./sha1.js', 'r') as f:
		js_sha1 = f.read()
	with open('./base64.js', 'r') as f:
		js_base64 = f.read()

	#
	# context = js2py.EvalJs()
	# context.execute(js_md5)
	# context.execute(js_sha1)
	# context.execute(js_base64)
	# context.vjkl5 = vjkl5
	# vl5x = context.execute(js_content)
	# guid = context.execute(js_guid)
	# print(vl5x, guid)
	# print('vl5x:', context.result)
	def get_guid():
		js = ""
		fp1 = open('./guid文件.js')
		js += fp1.read()
		fp1.close()
		ctx2 = execjs.compile(js)
		guid = (ctx2.call('Getguid'))
		print(guid)
		return guid

	def get_vl5x(vjkl5):
		# 根据vjkl5获取参数vl5x
		js = ""
		fp1 = open('./sha1.js')
		js += fp1.read()
		fp1.close()
		fp2 = open('./md5.js')
		js += fp2.read()
		fp2.close()
		fp3 = open('./base64.js')
		js += fp3.read()
		fp3.close()
		fp4 = open('./第一个.js')
		js += fp4.read()
		fp4.close()
		ctx2 = execjs.compile(js)
		vl5x = (ctx2.call('vl5x', vjkl5))
		print(vl5x)
		return vl5x

	return get_vl5x(vjkl5), get_guid()


if __name__ == '__main__':
	get('eb58acddb95fff16b67014a18656504888345f9b')
