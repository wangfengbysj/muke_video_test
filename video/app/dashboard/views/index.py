# encoding:utf-8
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class Index(View):
    TEMPLATE = 'dashboard/index.html'

    @dashboard_auth
    def get(self, request):
        return render_to_response(request,self.TEMPLATE)