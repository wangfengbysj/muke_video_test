# encoding:utf-8
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        to = request.GET.get('to','')

        get_token(request)
        data = {'error': '','to':to}
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to','')

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
        login(request, user)
        if to:
            return redirect(to)
        return redirect(reverse("dashboard_index"))

class AdminManager(View):
    TEMPLATE = '/dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        page = request.GET.get('page')
        if page:
            page = int(page)
        else:
            page = 1
        users = User.objects.all()
        paginator = Paginator(users, 3)
        page_num = paginator.num_pages
        page_user_list = paginator.get_page(page)
        if page_user_list.has_next():
            next_page = page + 1
        else:
            next_page = page

        if page_user_list.has_previous():
            previous_page = page - 1
        else:
            previous_page = page

        data = {
            'users': page_user_list,
            'page_num':range(1,page_num+1),
            'curr_page':page,
            'next_page':next_page,
            'previous_page':previous_page
        }
        print(users)
        return render_to_response(request, self.TEMPLATE, data=data)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('dashboard_login'))

class UpdateAdminStatus(View):
    def get(self,request):
        status = request.GET.get('status', 'on')
        print('status=',status)
        _status = True if status == 'on' else False
        request.user.is_superuser = _status
        request.user.save()
        return redirect(reverse('admin_manager'))
