import os
import subprocess
import sys

import cv2
import numpy
from moviepy import editor

VIDEO_OUTPUT_PATH = "output_remove_water_mark"
TEMP_VIDEO = "temp.mp4"


class WaterMarkUtils:
    def __init__(self, file_path: str, threshold: int, kernel_size: int):
        self.file_path = file_path
        # 阈值分割所用阈值
        self.threshold = threshold
        # 膨胀运算核尺寸
        self.kernel_size = kernel_size

    def remove_video_watermark(self):
        if not os.path.exists(VIDEO_OUTPUT_PATH):
            os.makedirs(VIDEO_OUTPUT_PATH)

        mask = self.__generate_watermark_mask()

        video = cv2.VideoCapture(self.file_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        size = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_writer = cv2.VideoWriter(TEMP_VIDEO, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

        success, frame = video.read()

        while success:
            frame = self.__inpaint_image(frame, mask)
            video_writer.write(frame)
            success, frame = video.read()
        video.release()
        video_writer.release()

        (_, file_name) = os.path.split(self.file_path)
        output_video_path = os.path.join(VIDEO_OUTPUT_PATH, file_name.split('.')[0] + "without_water_mark.mp4")
        output_audio_path = os.path.join(VIDEO_OUTPUT_PATH, file_name.split('.')[0] + "without_water_mark.mp3")
        self.__merge_audio(output_video_path, output_audio_path)

    # 截取视频多帧图像 生成多张水印，生成水印蒙版
    def __generate_watermark_mask(self) -> numpy.ndarray:
        video = cv2.VideoCapture(self.file_path)
        success, frame = video.read()
        roi = self.__select_roi(frame, "请圈选要去除的区域")
        print("圈选完毕", roi)
        mask = numpy.ones((frame.shape[0], frame.shape[1]), numpy.uint8)
        print("生成mask", mask)
        mask.fill(255)

        step = video.get(cv2.CAP_PROP_FRAME_COUNT) // 5
        index = 0
        while success:
            if index % step == 0:
                mask = cv2.bitwise_and(mask, self.__generate_single_mask(frame, roi, self.threshold))
            success, frame = video.read()
            index += 1
            print("if success ", success)
        video.release()
        print("video release ")
        return self.__dilate_mask(mask)

    def __select_roi(self, img: numpy.ndarray, hint: str) -> list:
        coff = 0.7
        w, h = int(coff * img.shape[1]), int(coff * img.shape[0])
        resize_img = cv2.resize(img, (w, h))
        roi = cv2.selectROI(hint, resize_img, False, False)
        print("选择完毕了ROI", roi)
        cv2.destroyAllWindows()
        watermark_roi = [int(roi[0] / coff), int(roi[1] / coff), int(roi[2] / coff), int(roi[3] / coff)]
        return watermark_roi

    # 通过手动选择的ROI区域生成单帧图像的水印蒙版
    # img 单帧图像
    # roi 手动选择的区域坐标
    # threshold 二值化阈值
    # 返回水印蒙版
    def __generate_single_mask(self, img: numpy.ndarray, roi: list, threshold: int) -> numpy.ndarray:
        if len(roi) != 4:
            print("ROI 错误，程序退出")
            sys.exit()
        roi_img = numpy.zeros((img.shape[0], img.shape[1]), numpy.uint8)
        start_x, end_x = int(roi[1]), int(roi[1] + roi[3])
        start_y, end_y = int(roi[0]), int(roi[0] + roi[2])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi_img[start_x:end_x, start_y:end_y] = gray[start_x:end_x, start_y:end_y]

        _, mask = cv2.threshold(roi_img, threshold, 255, cv2.THRESH_BINARY)
        return mask

    # 对蒙版进行膨胀运算
    # mask 蒙版图片
    # return 返回膨胀后的蒙版
    def __dilate_mask(self, mask: numpy.ndarray) -> numpy.ndarray:
        kernel = numpy.ones((self.kernel_size, self.kernel_size), numpy.uint8)
        mask = cv2.dilate(mask, kernel)
        return mask

    # 修复图像
    # img:单帧图像
    # mask:蒙版
    # return:返回的图像
    def __inpaint_image(self, img: numpy.ndarray, mask: numpy.ndarray) -> numpy.ndarray:
        telea = cv2.inpaint(img, mask, 1, cv2.INPAINT_TELEA)
        return telea

    def __merge_audio(self, output_video_path, output_audio_path):
        with editor.VideoFileClip(self.file_path) as video:
            clip = video.audio
            clip.write_audiofile(output_audio_path)
            subprocess.run(
                ['ffmpeg', '-i', TEMP_VIDEO, '-i', output_audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict',
                 'experimental', output_video_path])
