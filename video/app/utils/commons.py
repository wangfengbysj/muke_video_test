# encoding:utf-8

import os
import shutil
import time

from app.model.video import Video, VideoSub
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
    path_name = '/'.join([in_path, in_path_filename+"."+file_ext])
    shutil.copyfile(temp_file, path_name)

    # 拷贝path_out目录
    if file_ext == 'mp4':
        out_path = '/'.join([out_path, in_path_filename+".mp4"])
        print('is map4 path',out_path)
        shutil.copyfile(path_name,out_path)
    else:
        out_path = '/'.join([out_path,in_path_filename+'.mp4'])
        print('not map4 path', out_path)
        command = 'ffmpeg -i {} {}'.format(path_name, out_path)
        os.system(command)

    nginx_base_path = '/'.join([settings.NGINX_DIR, 'django_video'])
    path_name = '/'.join([nginx_base_path, in_path_filename+'.mp4'])
    shutil.copyfile(out_path, path_name)

    if os.path.exists(path_name):
        video = Video.objects.get(pk=video_id)
        print('save nginx path','/'.join([settings.VIDEO_HTTP, in_path_filename+'.mp4']))
        try:
            VideoSub.objects.create(
                video=video,
                url='/'.join([settings.VIDEO_HTTP, in_path_filename+'.mp4']),
                number=number
            )
            return True
        except:
            print('添加集数重复===============')
            return False
        finally:
            remove_path(['/'.join([in_path, in_path_filename + '.' + file_ext]),out_path])
    return False
