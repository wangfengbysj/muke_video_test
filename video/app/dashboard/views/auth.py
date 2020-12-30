# encoding:utf-8
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from app.libs.base_render import render_to_response


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        get_token(request)
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        data = {'error': ''}
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {}
        exists = User.objects.filter(username=username).exists()
        if not exists:
            data['error'] = '没有该用户'
            return render_to_response(request, self.TEMPLATE, data)
        user = authenticate(username=username, password=password)

        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data)

        if not user.is_superuser:
            data['error'] = '您没有权限登录'
            return render_to_response(request, self.TEMPLATE, data)
        login(request,user)
        return redirect(reverse("dashboard_index"))
