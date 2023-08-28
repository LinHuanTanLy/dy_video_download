# This is a sample Python script.
import asyncio

from utils.cv_utils import cut_frame_with_audio
from utils.dy_utils import DyUtils
from utils.ffmpeg_utils import video_do
from utils.file_utils import download_file

dy_url = "4.61 oDH:/ 复制打开抖音，看看黄泉杂货铺 # 因为一个片段看了整部剧 # 抖音短... https://v.douyin.com/iJvfFUsA/"
bi_number = "BV1wu4y1R7Le"
file_save_dy_path = "save/save_dy_video.mp4"
file_save_bi_path = "save/save_bi_video.mp4"


async def ffmpeg_video():
    video_do(file_save_dy_path)


async def frame_cut():
    cut_frame_with_audio(file_save_dy_path)


def __bi_download(download_url: str, headers):
    download_file(download_url, file_save_bi_path, headers=headers)
    print("download_url is ", download_url)


def __dy_download(download_url: str):
    download_file(download_url, file_save_dy_path)
    print("download_url is ", download_url)


def main():
    # BiUtils(bi_number, __bi_download).bi_download()
    DyUtils(dy_url, __dy_download).download_video()


if __name__ == '__main__':
    main()
