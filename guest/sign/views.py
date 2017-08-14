from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event

# Create your views here.
def index(request):
    return render(request,"index.html")

# 登录动作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['user'] = username # 添加浏览器 cookie
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    else:
        return render(request,'index.html',{'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '') # 读取浏览器 cookie
    return render(request,"event_manage.html",{"user":username,"events":event_list})
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username,"events": event_list})



