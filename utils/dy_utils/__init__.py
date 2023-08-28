import json
import re

import requests

from urls.urls import Urls
from utils import dy_headers
from utils.dy_utils.dy_encipher import getXbogus


class DyUtils:
    def __init__(self, url: str, callback):
        self.url = url
        self.aw_id = None
        self.callback = callback

    def download_video(self, ):
        # 1 获取短链
        short_link = self.__get_short_link()
        print("short link is ", short_link)

        # 2 获取request对象
        short_link_res = requests.get(short_link, headers=dy_headers)

        # 3 转义获取真实链接
        real_link = str(short_link_res.request.path_url)
        print("url_str " + real_link)

        # 4 获取aw_id
        aw_id = re.findall('video/(\d+)?', real_link)[0]
        self.aw_id = aw_id
        print("获取aw_id ", aw_id)

        # 5 通过aweme_id获取信息
        aw_info = self.__get_aw_info()

        # 6 获取url_list的第一个
        if aw_info is not None:
            # 6.1 打印相关信息
            url_first = aw_info["video"]["play_addr"]["url_list"][0]
            print("url is ", url_first)
            self.callback(url_first, )

    # 获取真正的短链
    def __get_short_link(self):
        return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.url)[0]

    # 获取作品信息
    def __get_aw_info(self, ):
        if self.aw_id is None:
            return None
        while True:
            try:
                payload = "aweme_id=" + self.aw_id + "&device_platform=webapp&aid=6383"
                print("format_url " + payload)
                single_video_url = Urls().POST_DETAIL + getXbogus(payload)
                raw = requests.get(url=single_video_url, headers=dy_headers).text
                print("get_aw_info raw " + raw)
                datadict = json.loads(raw)
                if datadict is not None and datadict["status_code"] == 0:
                    break
            except Exception as e:
                print('[报错] ' + e)
                return ""

        return datadict["aweme_detail"]
