# encoding:utf-8

from django.urls import path

from .views.index import Index
from .views.auth import Login, AdminManager, Logout, UpdateAdminStatus
from .views.video import ExternalVideo, VideoAddition, VideoStarView, VideoStarDelete, VideoSubDelete, VideoUpdate, \
    CustomVideo, CustomVideoAddtion

urlpatterns = [
    # 首页
    path('', Index.as_view(), name="dashboard_index"),
    # 登录认证
    path('login', Login.as_view(), name="dashboard_login"),
    path('logout', Logout.as_view(), name="logout"),
    # 用户管理
    path('admin/manager', AdminManager.as_view(), name="admin_manager"),
    path('admin/manager/update/status', UpdateAdminStatus.as_view(), name="admin_update_status"),

    # 外链视频
    path('video/external', ExternalVideo.as_view(), name='external_video'),
    # 编辑外链视频
    path('video/external/update/<int:video_id>', VideoUpdate.as_view(), name='external_video_update'),
    # 附加信息
    path('video/videosub/<int:video_id>', VideoAddition.as_view(), name='video_sub'),
    # 附加信息删除
    path('video/videosub/<int:video_id>/<int:videosub_id>', VideoSubDelete.as_view(), name='video_sub_del'),
    # 角色信息
    path('video/videostar/<int:video_id>', VideoStarView.as_view(), name='video_star'),
    # 角色删除
    path('video/videostar/<int:video_id>/<int:star_id>', VideoStarDelete.as_view(), name='video_star_delete'),

    #自制视频
    path('video/custom', CustomVideo.as_view(), name='custom_video'),
    #自制视频附加信息
    path('video/cust_video_sub/<int:video_id>', CustomVideoAddtion.as_view(),name='custom_video_sub')
]
