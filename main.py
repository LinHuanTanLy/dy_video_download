# This is a sample Python script.
import asyncio

from utils.cv_utils import cut_video_frame, cut_frame_with_audio
from utils.dy_utils import download_video
from utils.ffmpeg_utils import video_do
from pathlib import Path

dy_url = "3.58 RKj:/ 复制打开抖音，看看单纯大学生误入黄泉黑店？ 感性中年人满身秘密？ 红... https://v.douyin.com/iJWJ8GfC/"

file_save_path = "save/save_dy_video.mp4"


async def dy_download():
    download_video(dy_url, file_save_path)


async def ffmpeg_video():
    video_do(file_save_path)


async def frame_cut():
    cut_frame_with_audio(file_save_path)


async def main():
    file_path = Path(file_save_path)
    if file_path.is_file():
        await ffmpeg_video()
        await frame_cut()
    else:
        await dy_download()
        await ffmpeg_video()
        await frame_cut()


if __name__ == '__main__':
    asyncio.run(main())
