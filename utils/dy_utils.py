import json
import re
import time

import requests

from utils import dy_headers
from urls.urls import Urls
from utils.dy_encipher import getXbogus


def download_video(url):
    # 1 获取短链
    short_link = get_short_link(url)
    print("short link is " + short_link)

    # 2 获取request对象
    try:
        r = requests.get(short_link, headers=dy_headers)
    except Exception as e:
        print('[报错] ' + e)
        return ""

    # 3 转义获取真实链接
    url_str = str(r.request.path_url)
    print("url_str " + url_str)

    # 4 获取aweme_id
    aweme_id = get_aweme_id(url_str)
    print("aweme_id " + aweme_id)

    # 5 通过aweme_id获取信息
    aweme_info = get_aweme_info(aweme_id)
    print("测试数据", aweme_info['video']['play_addr']['url_list'][0])

    return ""


# 获取真正的短链
def get_short_link(long_url):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', long_url)[0]


# 获取aweme_id
def get_aweme_id(url_str):
    aweme_id = re.findall('video/(\d+)?', url_str)[0]
    return aweme_id


# 获取作品信息
def get_aweme_info(aweme_id):
    if aweme_id is None:
        return None
    start_time = time.time()
    while True:
        try:
            payload = "aweme_id=" + aweme_id + "&device_platform=webapp&aid=6383"
            print("format_url " + payload)
            single_video_url = Urls().POST_DETAIL + getXbogus(payload)
            raw = requests.get(url=single_video_url, headers=dy_headers).text
            print("get_aweme_info raw " + raw)
            datadict = json.loads(raw)
            if datadict is not None and datadict["status_code"] == 0:
                end_time = time.time()
                break
        except Exception as e:
            print('[报错] ' + e)
            return ""

    elapsed_time = end_time - start_time  # 计算耗时（以秒为单位）

    print("获取成功，耗时", elapsed_time, 's')
    return datadict["aweme_detail"]
