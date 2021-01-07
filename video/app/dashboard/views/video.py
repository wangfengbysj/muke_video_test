# encoding:utf-8
from django.db import IntegrityError
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from app.libs.base_render import render_to_response
from app.model.video import Video
from app.utils.permission import dashboard_auth


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
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get("info")
        if not all([name, image, video_type, from_to, nationality, info]):
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
