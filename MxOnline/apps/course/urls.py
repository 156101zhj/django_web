from django.conf.urls import url, include


from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView,VideoPlayView


urlpatterns = [
    #这是课程列表页
    url(r'^list/$',CourseListView.as_view(),name='course_list'),

    #这是课程详情页
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),


    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),

    # 这是课程评论页
    url(r'^comment/(?P<course_id>\d+)/$',CommentsView.as_view(),name='course_comment'),

    #添加用户评论
    url(r'^add_comment/$',AddCommentsView.as_view(),name='add_comment'),

    # 课程视频播放页
    url('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),

]