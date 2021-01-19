# encoding:utf-8

import os
import shutil
import time

from app.model.video import Video, VideoSub
from config import settings


def handle_video(video_file,video_id, number):
    # path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp')
    path = '/'.join([settings.NGINX_DIR, 'django_video'])
    name = '{}_{}'.format(time.time(),video_file.name)
    path_name = '/'.join([path,name])
    temp_path = video_file.temporary_file_path()
    shutil.copyfile(temp_path, path_name)

    if os.path.exists(path_name):
        video = Video.objects.get(pk=video_id)
        try:
            VideoSub.objects.create(
                video=video,
                url='/'.join([settings.VIDEO_HTTP, name]),
                number=number
            )
            return True
        except:
            return False
    return False

