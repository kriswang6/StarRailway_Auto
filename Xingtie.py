# -*- encoding=utf8 -*-
__author__ = "admin"

from airtest.core.api import *
from airtest.aircv import *
from airtest.report.report import simple_report

import sys
import json
import base64
import random
import datetime
import time

auto_setup(__file__,devices=["Windows:///"])
#-----------------函数区
def test_ocr(filename):
    # 保证兼容python2以及python3
    IS_PY3 = sys.version_info.major == 3
    if IS_PY3:
        from urllib.request import urlopen
        from urllib.request import Request
        from urllib.error import URLError
        from urllib.parse import urlencode
        from urllib.parse import quote_plus
    else:
        import urllib2
        from urllib import quote_plus
        from urllib2 import urlopen
        from urllib2 import Request
        from urllib2 import URLError
        from urllib import urlencode

    # 防止https证书校验不正确
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    API_KEY = 'r9V8wonkzCYGRulhA2qIRyrs'

    SECRET_KEY = '3oOyWgb9KFWY126YgdxS6a0G0xf6Y3LA'


    OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"


    """  TOKEN start """
    TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


    """
        获取token
    """
    def fetch_token():
        params = {'grant_type': 'client_credentials',
                  'client_id': API_KEY,
                  'client_secret': SECRET_KEY}
        post_data = urlencode(params)
        if (IS_PY3):
            post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            print(err)
        if (IS_PY3):
            result_str = result_str.decode()


        result = json.loads(result_str)

        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not 'brain_all_scope' in result['scope'].split(' '):
                print ('please ensure has check the  ability')
                exit()
            return result['access_token']
        else:
            print ('please overwrite the correct API_KEY and SECRET_KEY')
            exit()

    """
        读取文件
    """
    def read_file(image_path):
        f = None
        try:
            f = open(image_path, 'rb')
            return f.read()
        except:
            print('read image file fail')
            return None
        finally:
            if f:
                f.close()


    """
        调用远程服务
    """
    def request(url, data):
        req = Request(url, data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()
            if (IS_PY3):
                result_str = result_str.decode()
            return result_str
        except  URLError as err:
            print(err)

    if __name__ == '__main__':

        # 获取access token
        token = fetch_token()

        # 拼接通用文字识别高精度url
        image_url = OCR_URL + "?access_token=" + token

        text = ""

        # 读取测试图片
        file_content = read_file(filename)

        # 调用文字识别服务
        result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

        # 解析返回结果
        result_json = json.loads(result)
        for words_result in result_json["words_result"]:
            text = text + words_result["words"]

        # 打印文字
        return text
    
def touch_plus(t,x1,y1,x2,y2):
    
    screen = G.DEVICE.snapshot()
    local_screen = aircv.crop_image(screen,(x1,y1,x2,y2))

    # 将我们的目标截图设置为一个Template对象

    # 在局部截图里面查找指定的图片对象
    pos = t.match_in(local_screen)
    while not(pos):
        screen = G.DEVICE.snapshot()
        local_screen = aircv.crop_image(screen,(x1,y1,x2,y2))

        # 将我们的目标截图设置为一个Template对象

        # 在局部截图里面查找指定的图片对象
        pos = t.match_in(local_screen)

    touch((x1 + pos[0],y1 + pos[1]))
    
def wait_plus(t,x1,y1,x2,y2):

    screen = G.DEVICE.snapshot()
    local_screen = aircv.crop_image(screen,(x1,y1,x2,y2))
    pil_image = cv2_2_pil(local_screen)
    pil_image.save("wait.png", quality=99, optimize=True)
    # 将我们的目标截图设置为一个Template对象

    # 在局部截图里面查找指定的图片对象
    pos = t.match_in(local_screen)
    while not(pos):
        screen = G.DEVICE.snapshot()
        local_screen = aircv.crop_image(screen,(x1,y1,x2,y2))
        pil_image = cv2_2_pil(local_screen)
        pil_image.save("wait.png", quality=99, optimize=True)
        # 将我们的目标截图设置为一个Template对象

        # 在局部截图里面查找指定的图片对象
        pos = t.match_in(local_screen)
    return

def ColdStartApp(): #指从桌面启动游戏开始
    
    touch_plus(Template(r"DianJiJinRu.png"),623,701,746,744)
    
    
# def WarmStartApp():
    
#--------------------程序区

ColdStartApp()
