"""online_course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
import xadmin

import users.urls as url_user
from django.views.static import serve
from .settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('',  TemplateView.as_view(template_name='indexs/index.html'),name='index'),
    path('users/',include(url_user)),
    path('org/',include('organization.urls')),
    #验证码
    path('captcha/',include('captcha.urls')),
    #处理路径里有media文件时的路由
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
