from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.backends import ModelBackend
from .models import UserProfile
from django.db.models import Q

from .form import LoginForm

#邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# def user_login(request):
#     if request.method == 'POST':
#         # 获取用户提交的用户名和密码
#         user_name = request.POST.get('username', None)
#         pass_word = request.POST.get('password', None)
#         # 成功返回user对象,失败None
#         user = authenticate(username=user_name, password=pass_word)
#         # 如果不是null说明验证成功
#         if user is not None:
#             # 登录
#             login(request, user)
#             return render(request, 'indexs/index.html')
#         else:
#             return render(request, 'users/login.html', {'msg': '用户名或密码错误'})
#     elif request.method == 'GET':
#         return render(request, 'users/login.html')


#把前面views中的user_login()函数改成基于类的形式
from django.views.generic.base import View


class LoginView(View):
    #响应get方法，获取html
    def get(self,request):
        return render(request, 'users/login.html')


    #响应post，点击注册时的响应
    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username', None)
            pass_word = request.POST.get('password', None)
            # 成功返回user对象,失败None
            user = authenticate(username=user_name, password=pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                # 登录
                login(request, user)
                return render(request, 'indexs/index.html')
            else:
                return render(request, 'users/login.html', {'msg': '用户名或密码错误'})
        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


from .form import *
from utils.email_send import send_register_eamil
class RegisterView(View):
    '''用户注册'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'users/register.html',{'register_form':register_form})


    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已存在'})

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.email = email
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            #发送邮件
            if send_register_eamil(email=email,send_type="register"):
                return render(request, 'users/login.html')
            else:
                return render(request, 'users/register.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})

# 激活用户
from users.models import EmailVerifyRecord
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
         # 验证码不对的时候跳转到激活失败页面
        else:
            return render(request,'active_fail.html')
        # 激活成功跳转到登录页面
        return render(request, "login.html", )


from .form import ForgetPwdForm
#忘记密码    返回填写邮箱账号html
class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request,'users/forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email',None)
            send_register_eamil(email,'forget')
            return render(request, 'users/send_success.html')
        else:
            return render(request,'users/forgetpwd.html',{'forget_form':forget_form})

#点击重置密码链接    返回密码html
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "users/password_reset.html", {"email":email})
        else:
            return render(request, "users/active_fail.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "users/password_reset.html", {"email":email, "msg":"密码不一致！"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, "users/login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "users/password_reset.html", {"email":email, "modify_form":modify_form })
