from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def user_logout(request):
    logout


def user_logout(request):
    logout(request)
    return redirect("profile")


def user_profile(request):

    return render(request, "user/profile.html", {"user": request.user})


# Create your views here.
def user_login(request):
    message = ""
    if request.method == "POST":
        if request.POST.get("register"):
            return redirect("register")

        elif request.POST.get("login"):
            username = request.POST.get("username")
            password = request.POST.get("password")

            if username == "" or password == "":
                message = "帳號或密碼不能為空!"
            else:
                # 登入
                user = authenticate(request, username=username, password=password)
                print(user, username, password)
                if user:
                    login(request, user)
                    message = " 登入成功!"
                    return redirect("todo")

                else:
                    message = "帳號或密碼錯誤!"

    return render(request, "user/login.html", {"message": message})


def user_register(request):
    message = ""
    form = UserCreationForm()
    # 取得所有all
    # 取得唯一get
    # 取得篩選filter
    print(User.objects.filter(username="zoe"))
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        # print(username, password1, password2)

    try:
        if len(password1) < 8:
            message = "密碼長度至少要8個字元"
        elif password1 != password2:
            message = "兩次密碼不符"
        else:
            # 檢查使用者帳號是否存在
            user = User.objects.filter(username=username)
            if len(user) > 0:
                message = "帳號已經存在!"
            else:
                User.objects.create_user(username=username, password=password1).save()
                message = "註冊成功!"
    except Exception as e:
        print(e)
        message = "請洽網站管理員"

    return render(request, "user/register.html", {"form": form, "message": message})
