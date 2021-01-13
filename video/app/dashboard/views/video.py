# encoding:utf-8
import json

from django.core import serializers
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from app.libs.base_render import render_to_response
from app.model.video import Video, FromType, VideoSub, VideoStar
from app.utils.permission import dashboard_auth


# 外链接页面
class ExternalVideo(View):
    TEMPLATE = '/dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):
        error = request.GET.get('error')
        success = request.GET.get('success')
        if error:
            data = {'error': error}
        elif success:
            data = {'success': success}
        else:
            data = {}

        videos = Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get("info")
        video_id = request.POST.get('video_id')
        if not all([name, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(reverse('external_video'), '缺少必要字段 '))
        print(name, image, video_type, from_to, nationality, info)

        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=video_type,
                    from_to=from_to,
                    nationality=nationality,
                    info=info
                )
            except IntegrityError as e:
                return redirect('{}?error={}'.format(reverse('external_video'), '添加视频数据重复'))
        else:
            try:
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = image
                video.video_type = video_type
                video.from_to=from_to
                video.nationality = nationality
                video.info = info
                video.save()
            except:
                return redirect('{}?error={}'.format(reverse('external_video'), '更新视频数据重复'))

        return redirect('{}?success={}'.format(reverse('external_video'), '操作成功'))


# 外部视频->附加信息
class VideoAddition(View):
    TEMPLATE = '/dashboard/video/video_sub.html'

    def get(self, request, video_id):
        data = {}
        data['video'] = Video.objects.get(pk=video_id)
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        url = request.POST.get('url')
        number = request.POST.get('number')
        video_sub_id = request.POST.get('videosub_id')

        if url == '' or number == '':
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))

        if not video_sub_id:
            video = Video.objects.get(pk=video_id)
            VideoSub.objects.create(video=video, url=url, number=number)
            return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '添加演员成功'))
        else:
            video_sub = VideoSub.objects.get(pk=video_sub_id)
            video_sub.url = url
            video_sub.number = number
            video_sub.save()
            return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '编辑演员成功'))


# 外部链接->添加角色
class VideoStarView(View):

    def post(self, request, video_id):
        name = request.POST.get('actorName')
        identity = request.POST.get('identity')
        print(name, identity, video_id)
        if not all([name, identity]):
            return redirect('{}?error={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '缺少必要字段 '))

        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(
                name=name,
                identity=identity,
                video=video
            )
        except:
            return redirect('{}?error={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '演员添加失败'))

        return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '演员添加成功'))


# 外部链接->角色删除
class VideoStarDelete(View):

    def get(self, request, star_id, video_id):
        star = VideoStar.objects.get(pk=star_id)
        if star:
            star.delete()
        return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '演员删除成功'))


# 外部链接->删除附加信息
class VideoSubDelete(View):
    def get(self, request, video_id, videosub_id):
        VideoSub.objects.get(pk=videosub_id).delete()
        return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '删除附加信息成功'))


class VideoUpdate(View):
    def get(self, request, video_id):
        print('video_id=', video_id)
        video = Video.objects.get(pk=video_id)
        # Video对象转换成json字符串数组
        videos_str = serializers.serialize('json', [video, ])
        # 字符串转换成json对象，并获取第一个数字对象
        video_obj = json.loads(videos_str)[0]
        return JsonResponse(video_obj)
