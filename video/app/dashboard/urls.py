# encoding:utf-8

from django.urls import path

from .views.index import Index
from .views.auth import Login

urlpatterns = [
    path('', Index.as_view(), name="dashboard_index"),
    path('login', Login.as_view(), name="dashboard_login")
]