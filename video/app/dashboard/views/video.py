# encoding:utf-8
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class ExternalVideo(View):
    TEMPLATE = '/dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):
        return render_to_response(request, self.TEMPLATE)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get("info")

        print(name, image, video_type, from_to, nationality, info)
        return redirect(reverse('external_video'))