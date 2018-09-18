from django.conf.urls import url, include
from .views import UserinfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

from .views import MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView

urlpatterns = [
    #用户信息
    url(r'^info/$',UserinfoView.as_view(),name='user_info'),

    #用户图像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload'),

    #用户密码修改
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name='update_pwd'),

    #发送邮箱验证码
    url(r'^sendemail_code/$',SendEmailCodeView.as_view(),name='sendemail_code'),

    #修改邮箱
    url(r"^update_email/$", UpdateEmailView.as_view(),name='update_email'),

    #我的课程
    url(r"^mycourse/$", MyCourseView.as_view(),name='mycourse'),

    #我的收藏
    url(r"^myfav/org/$", MyFavOrgView.as_view(),name='myfav_org'),

    #我的收藏教师
    url(r"^myfav/teacher/$", MyFavTeacherView.as_view(),name='myfav_teacher'),

    #我的收藏公开课
    url(r"^myfav/course/$", MyFavCourseView.as_view(),name='myfav_course'),

    # 我的消息
    url(r"^mymessage/$", MyMessageView.as_view(), name='mymessage'),

]
