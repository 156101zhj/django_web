from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q


from operation.models import UserFavorite
from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from course.models import Course
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.



class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        org_page = 'org'

        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        #城市
        all_citys = CityDict.objects.all()

        # 取出机构搜索关键词
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # 使用django中的搜索功能name__icontains会转换为sql的like语句
            all_orgs = all_orgs.filter(
                Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))


        #取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别刷选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        #排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)


        return render(request,"org-list.html",{
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id" : city_id,
            "category" : category,
            "hot_orgs" : hot_orgs,
            "sort" : sort,
            "org_page":org_page

        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            #通过moudle调用，直接存储到数据库
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错！"}',content_type='application/json')


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        current_page = 'home'

        course_org = CourseOrg.objects.get(id = int(org_id))

        course_org.click_nums += 1
        course_org.save()

        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request,"org-detail-homepage.html",{
            "all_courses" : all_courses,
            "all_teachers" : all_teachers,
            "course_org" : course_org,
            "current_page" : current_page,
            'has_fav' : has_fav
        })

class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()

        return render(request,"org-detail-course.html",{
            "all_courses" : all_courses,
            "current_page": current_page,
            "course_org" : course_org,
            'has_fav': has_fav
        })

class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request,"org-detail-desc.html",{
            "current_page": current_page,
            "course_org" : course_org,
            'has_fav': has_fav
        })

class OrgTeacherView(View):
    '''
    机构讲师列表页
    '''
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id = int(org_id))
        # 判断收藏状态
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()

        return render(request,"org-detail-teachers.html",{
            "all_teachers" : all_teachers,
            "current_page": current_page,
            "course_org" : course_org,
            'has_fav': has_fav
        })


class AddFavView(View):
    """
    用户收藏和取消收藏
    """
    def post(self, request):
        id = request.POST.get('fav_id', 0)         # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)     # 防止int(fav_type)出错

        #判断用户是否登录
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))

        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -=1
                if course.fav_nums <0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                course_org = CourseOrg.objects.get(id=int(id))
                course_org.fav_nums -=1
                if course_org.fav_nums <0:
                    course_org.fav_nums = 0
                course_org.save()
            elif int(type) == 3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -=1
                if teacher.fav_nums <0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')


        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()

                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    course_org = CourseOrg.objects.get(id=int(id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(type) == 3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

'''


'''

# 讲师列表
class TeacherListView(LoginRequiredMixin,View):
    def get(self, request):
        all_teachers = Teacher.objects.all()

        teacher_page = "teacher"

        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teachers = all_teachers.filter(name__icontains=search_keywords)
        # 人气排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
            "teacher_page": teacher_page,
        })

class TeacherDetailView(View):
    def get(self, request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()

        all_courses = Course.objects.filter(teacher=teacher)

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        return render(request, "teacher-detail.html", {
            "teacher" : teacher,
            "all_courses":all_courses,
            "sorted_teachers": sorted_teachers,
            "has_teacher_faved" : has_teacher_faved,
            "has_org_faved" : has_org_faved

        })

















