# encoding:utf-8
from django.db import IntegrityError
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
        if not all([name, video_type, from_to, nationality, info]):
            return redirect('{}?error={}'.format(reverse('external_video'), '缺少必要字段 '))
        print(name, image, video_type, from_to, nationality, info)

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
            return redirect('{}?error={}'.format(reverse('external_video'), '视频数据重复'))

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
        if url == '':
            return redirect(reverse('video_sub', kwargs={'video_id': video_id}))
        else:
            video = Video.objects.get(pk=video_id)
            length = video.video_sub.count()
            VideoSub.objects.create(video=video, url=url,number=length + 1)
            return redirect(reverse('video_sub', kwargs={'video_id':video_id}))

#w外部链接->添加角色
class VideoStarView(View):

    def post(self,request,video_id):
        name = request.POST.get('actorName')
        identity = request.POST.get('identity')
        print(name, identity, video_id)
        if not all([name,identity]):
            return redirect('{}?error={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '缺少必要字段 '))

        video = Video.objects.get(pk=video_id)
        try:
            VideoStar.objects.create(
                name=name,
                identity=identity,
                video=video
            )
        except :
            return redirect('{}?error={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '演员添加失败'))

        return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '演员添加成功'))

class VideoStarDelete(View):

    def get(self, request, star_id,video_id):
        star = VideoStar.objects.get(pk=star_id)
        if star:
            star.delete()
        return redirect('{}?success={}'.format(reverse('video_sub', kwargs={'video_id': video_id}), '演员删除成功'))
