# This is a sample Python script.
from utils.dy_utils import download_video

dy_url = "8.43 CHv:/ 复制打开抖音，看看# 因为一个片段看了整部剧 # 热门短剧推荐 # ... https://v.douyin.com/iJG5kbJN/";


def dy_download(url):
    download_video(url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dy_download(dy_url)
