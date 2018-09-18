"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

#该导入是通过函数来实现登录
# from users.views import user_login
from  users.views import LoginView,LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT

from users.views import IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #通过as_view方法将静态页面转换views函数
    url('^$',IndexView.as_view(),name="index"),
    # url('^login/$', user_login,name="login"),
    url('^login/$', LoginView.as_view(),name="login"),
    #退出
    url('^logout/$', LogoutView.as_view(),name="logout"),
    url('^register/$', RegisterView.as_view(),name="register"),
    url(r'^captcha/',include('captcha.urls')),
    url('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),
    url('^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),
    url('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    url('^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),



    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve,{"document_root":MEDIA_ROOT}),

    #生产环境下静态文件访问处理函数
    # url(r'^static/(?P<path>.*)$', serve,{"document_root":STATIC_ROOT}),

    #课程机构url配置
    url(r"^org/",include('organization.urls',namespace='org')),

    #课程相关url配置
    url(r"^course/",include('course.urls',namespace='course')),

    #课程机构url配置 访问路径是uesrs/info/
    url(r"^users/",include('users.urls',namespace='users')),

    #富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls'))


]

#全局404配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'