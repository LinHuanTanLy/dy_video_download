import os
import subprocess

import cv2
import numpy as np

from utils.file_utils import is_exist_file


# 对视频进行抽帧检测
# 如果相似度高于[similarity_threshold]，则去除
def cut_video_frame(file_path: str):
    frame_rate = 30
    output_video = None
    is_exist = is_exist_file(file_path)
    if file_path is not None and is_exist:
        video_capture = cv2.VideoCapture(file_path)

        if not video_capture.isOpened():
            print("无法打开视频文件")
            return

        unique_frames = []
        similarity_threshold = 0.90  # 可根据需要调整
        prev_frame = None
        first_frame = None
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            if prev_frame is None:
                prev_frame = frame
                first_frame = frame
                unique_frames.append(frame)
                continue

            diff = cv2.absdiff(prev_frame, frame)
            similarity = np.mean(diff)
            print("进行帧比较，当前帧差异为", str(similarity < similarity_threshold))
            if similarity < similarity_threshold:
                unique_frames.append(frame)
            prev_frame = frame

        video_capture.release()
        cv2.destroyAllWindows()
        print("进行帧比较完毕，目前帧数为", str(len(unique_frames)))
        if output_video is None:
            height, width, _ = first_frame.shape
            output_video = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

        output_video.write(frame)

        print("进行帧比较完毕，开始整合视频")
        index = 0
        total = len(unique_frames)
        for frame in unique_frames:
            output_video.write(frame)
            print("进行帧比较完毕，开始整合视频", str(index / total))
            index += 1
        output_video.release()
        print("进行帧比较完毕，开始输出视频")
    else:
        print("file is empty")


def cut_frame_with_audio(input_video_path):
    output_audio_path = "save/output_audio.aac"
    output_video_path = "save/output.mp4"
    final_output_video_path = "save/final_output.mp4"

    # 移除的帧数
    cut_frame_count = 0
    # 最大差别的帧差异
    max_frame_diff = 0

    check_file(output_video_path)
    check_file(output_audio_path)
    check_file(final_output_video_path)
    # 提取视频帧
    video_capture = cv2.VideoCapture(input_video_path)
    if not video_capture.isOpened():
        print("无法打开视频文件")
        return

    frame_rate = int(video_capture.get(cv2.CAP_PROP_FPS))  # 获取原始视频的帧率
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (frame_width, frame_height))

    unique_frames = []
    similarity_threshold = 55  # 可根据需要调整
    prev_frame = None

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        if prev_frame is None:
            prev_frame = frame
            unique_frames.append(frame)
            continue

        diff = cv2.absdiff(prev_frame, frame)
        similarity = np.mean(diff)
        if similarity > max_frame_diff:
            max_frame_diff = similarity
        print("进行帧比较，当前帧差异为", str(similarity), "是否抛弃这一帧", str(similarity >= similarity_threshold))
        if similarity < similarity_threshold:
            unique_frames.append(frame)
        else:
            cut_frame_count += 1
        prev_frame = frame

    video_capture.release()
    cv2.destroyAllWindows()
    print("进行帧比较完毕，目前帧数为", str(len(unique_frames)), "一共移除了", cut_frame_count, "帧",
          "其中最大的帧差异为", max_frame_diff)

    index = 0
    total = len(unique_frames)
    # 写入视频帧
    for frame in unique_frames:
        output_video.write(frame)
        print("正在整合视频，当前进度为", index, "/", total)
        index += 1

    output_video.release()
    print("视频帧写入完毕")

    # 提取音频
    subprocess.run(['ffmpeg', '-i', input_video_path, '-vn', '-acodec', 'aac', output_audio_path])
    print("音频提取完毕")

    # 合并音频和视频
    subprocess.run(
        ['ffmpeg', '-i', output_video_path, '-i', output_audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict',
         'experimental', final_output_video_path])
    print("音频与视频合并完毕")


# 检查输出目录是否存在，如果不存在则创建
def check_file(file_path):
    output_directory = os.path.dirname(file_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
