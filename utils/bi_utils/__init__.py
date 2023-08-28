import json

import requests
from utils import bi_headers


class BiUtils:

    def __init__(self, url, callback):
        self.url = url
        self.callback = callback

    # 下载哔哩哔哩视频
    def bi_download(self, ):
        self.__get_c_id(callback=self.__get_video_url)

    # 获取视频的链接
    def __get_video_url(self, c_id: str):
        url = f"https://api.bilibili.com/x/player/playurl?avid=&cid={c_id}&bvid={self.url}&qn=240&type=&otype=json"
        res = requests.get(url, headers=bi_headers)
        if res.status_code == 200 and res.text is not None:
            video_url = json.loads(res.text)["data"]["durl"][0]["url"]
            self.callback(video_url, bi_headers)

    # 获取视频的c_id
    def __get_c_id(self, callback):
        c_url = f"https://api.bilibili.com/x/player/pagelist?bvid={self.url}&jsonp=jsonp"
        res = requests.get(c_url, headers=bi_headers)
        if res.status_code == 200 and res.text is not None:
            c_id = json.loads(res.text)['data'][0]['cid']
            callback(c_id, )
        else:
            return ""
