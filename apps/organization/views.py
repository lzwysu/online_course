from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from pure_pagination import Paginator,PageNotAnInteger
from .models import *
class OrgView(View):
    '''课程机构'''
    def get(self,request):
        citys=CityDict.objects.all()
        course_orgs=CourseOrg.objects.all()
        org_num=course_orgs.count()
        try:
            page_nume = request.GET.get('page', 1)
        except PageNotAnInteger:
            page_nume=1
        p = Paginator(course_orgs, 3, request=request)
        course_orgs_page=p.page(page_nume)

        return render(request,'organizations/org-list.html',locals())

