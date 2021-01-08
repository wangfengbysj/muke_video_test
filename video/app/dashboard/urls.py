# encoding:utf-8

from django.urls import path

from .views.index import Index
from .views.auth import Login, AdminManager, Logout, UpdateAdminStatus
from .views.video import ExternalVideo,VideoAddition

urlpatterns = [
    # 首页
    path('', Index.as_view(), name="dashboard_index"),
    # 登录认证
    path('login', Login.as_view(), name="dashboard_login"),
    path('logout', Logout.as_view(), name="logout"),
    # 用户管理
    path('admin/manager', AdminManager.as_view(), name="admin_manager"),
    path('admin/manager/update/status',UpdateAdminStatus.as_view(),name="admin_update_status"),

    # 外链视频
    path('video/external', ExternalVideo.as_view(), name='external_video'),
    # 附加信息
    path('video/videosub/<int:video_id>',VideoAddition.as_view(), name='video_sub' )
]