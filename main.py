# This is a sample Python script.
import asyncio

from utils.bi_utils import BiUtils
from utils.cv_utils import cut_frame_with_audio
from utils.dy_utils import DyUtils
from utils.ffmpeg_utils import video_do
from utils.file_utils import download_file
from utils.water_mark_utils import WaterMarkUtils

dy_url = "4.61 oDH:/ 复制打开抖音，看看黄泉杂货铺 # 因为一个片段看了整部剧 # 抖音短... https://v.douyin.com/iJvfFUsA/"
bi_number = "BV1wu4y1R7Le"
file_save_dy_path = "save/save_dy_video.mp4"
file_save_bi_path = "save/save_bi_video.mp4"
file_with_water_mark = "water_mark_video.mp4"


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


def __remove_water_mark():
    WaterMarkUtils(file_with_water_mark, threshold=80, kernel_size=5).remove_video_watermark()


def __download_dy_video():
    dy_video_url = input("请输入要下载的视频链接:\n")
    if dy_video_url is None or dy_video_url == "":
        print("请提供完整的下载链接")
        exit()
    else:
        DyUtils(dy_video_url, __dy_download).download_video()


def __download_bi_video():
    bi_video_number = input("请输入要下载的B站BV号:\n")
    if bi_video_number is None or bi_video_number == "":
        print("请提供完整的B站BV号")
        exit()
    else:
        BiUtils(bi_video_number, __bi_download).bi_download()


if __name__ == '__main__':
    option_type = input("你要做什么：\n 1.下载抖音视频 \n 2.下载B站视频 \n 3.视频去水印 \n")
    if option_type == "3":
        __remove_water_mark()
    elif option_type == "1":
        __download_dy_video()
    elif option_type == "2":
        __download_bi_video()
