from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from pure_pagination import Paginator,PageNotAnInteger
from .models import *

from django.http import HttpResponse
from .forms import UserAskForm



class OrgView(View):
    '''课程机构'''
    def get(self,request):
        #所有城市
        citys=CityDict.objects.all()
        # 所有机构
        course_orgs=CourseOrg.objects.all()

        # 热门课程机构排名
        hot_orgs = course_orgs.order_by('-click_nums')[:5]

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            course_orgs = course_orgs.filter(category=category)

        #城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            course_orgs = course_orgs.filter(city_id=int(city_id))

        # 学习人数和课程数筛选
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                course_orgs = course_orgs.order_by("-students")
            elif sort == "courses":
                course_orgs = course_orgs.order_by("-course_nums")

        # 机构数目
        org_num = course_orgs.count()

        #分页
        try:
            page_nume = request.GET.get('page', 1)
        except PageNotAnInteger:
            page_nume=1
        p = Paginator(course_orgs, 4, request=request)
        course_orgs_page=p.page(page_nume)

        return render(request,'organizations/org-list.html',locals())


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    '''机构首页'''
    def get(self,request,org_id):
        # 根据id找到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request,'org-detail-homepage.html',{
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
        })