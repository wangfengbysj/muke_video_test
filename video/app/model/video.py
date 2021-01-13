# encoding:utf-8
import time
from enum import Enum

from django.db import models

# 视频类型
class VideoType(Enum):
    movie = 'movie'
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'vareity'
    other = 'other'


VideoType.movie.label = '电影'
VideoType.cartoon.label = '卡通'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'

# 视频类型
class FromType(Enum):
    youku = 'youku'
    custom = 'custom'


FromType.youku.label = '优酷'
FromType.custom.label = '自制'

# 视频国籍
class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'


NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.korea.label = '韩国'
NationalityType.america.label = '美国 '
NationalityType.other.label = '其他'

# 演员类型
class IdentityType(Enum):
    director = 'director'
    protagonist = 'protagonist'
    minorroles = 'minorroles'

IdentityType.director.label='导演'
IdentityType.protagonist.label='主角'
IdentityType.minorroles.label='配角'
IdentityType.director.color='primary'
IdentityType.protagonist.color='success'
IdentityType.minorroles.color='info'

# 视频对象
class Video(models.Model):
    name = models.CharField(max_length=100, null=False)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    from_to = models.CharField(max_length=20, null=False, default=FromType.custom.value)
    nationality = models.CharField(max_length=20, null=False, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'video_type', 'from_to', 'nationality']
    @property
    def createdtm(self):
        return self.created_time.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def updatedtm(self):
        return self.updated_time.strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        return self.name


# 视频演员
class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ['video', 'name', 'identity']

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True, null=True)
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ['video', 'number']

    def __str__(self):
        return 'video:{}, number:{}'.format(self.video.name, self.number)