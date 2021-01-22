# coding:utf-8
import os
import shutil

from celery import task
from django.db import IntegrityError

from app.model.video import VideoSub

from config import settings


@task
def video_task(in_path, file_ext, out_path, in_path_filename, path_name, videosub_id):

    from app.utils.commons import remove_path
    # 拷贝path_out目录
    if file_ext == 'mp4':
        out_path = '/'.join([out_path, in_path_filename + ".mp4"])
        shutil.copyfile(path_name, out_path)
    else:
        out_path = '/'.join([out_path, in_path_filename + '.mp4'])
        command = 'ffmpeg -i {} {}'.format(path_name, out_path)
        os.system(command)

    nginx_base_path = '/'.join([settings.NGINX_DIR, 'django_video'])
    path_name = '/'.join([nginx_base_path, in_path_filename + '.mp4'])
    shutil.copyfile(out_path, path_name)

    if os.path.exists(path_name):
        videosub = VideoSub.objects.get(pk=videosub_id)
        try:
            videosub.url = '/'.join([settings.VIDEO_HTTP, in_path_filename + '.mp4'])
            videosub.save()
            return True
        except IntegrityError as e:
            remove_path(['/'.join([settings.NGINX_DIR, 'django_video', in_path_filename + '.mp4'])])
            return False
        finally:
            remove_path(['/'.join([in_path, in_path_filename + '.' + file_ext]), out_path])
        return False
