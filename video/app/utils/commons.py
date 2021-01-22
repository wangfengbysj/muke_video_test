# coding:utf-8

import os
import shutil
import time

from app.model.video import Video, VideoSub
from app.tasks.task import video_task
from config import settings


# 删除多个文件
def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


# 视频文件读取并保存到nginx代理目录
def handle_video(video_file, video_id, number):
    in_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_out')
    temp_file = video_file.temporary_file_path()
    filename = video_file.name.split(".")[0]
    file_ext = video_file.name.split(".")[1]

    # 上传path_in目录
    in_path_filename = '{}_{}'.format(time.time(), filename)
    path_name = '/'.join([in_path, in_path_filename + "." + file_ext])
    shutil.copyfile(temp_file, path_name)

    video = Video.objects.get(pk=video_id)
    videosub = VideoSub.objects.create(
        video=video,
        url='',
        number=number
    )
    return video_task.delay(in_path, file_ext, out_path, in_path_filename, path_name, videosub.id)
