from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, "index.html")


# 登录动作
@login_required
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username  # 添加浏览器 cookie
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})
    else:
        return render(request, 'index.html', {'error': 'username or password error!'})


# 发布会管理
@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')  # 读取浏览器 cookie
    return render(request, "event_manage.html", {"user": username, "events": event_list})

@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get("name", "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If  page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    return render(request, "guest_manage.html", {"user": username, "guests": contacts})


# 签到页面
@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    a = Event.objects.filter(id = event_id)
    guest_list = Guest.objects.filter(event_id = a)
    p = Paginator(guest_list, 2)
    tt = p.count
    t = 0
    for guest in guest_list:
        if guest.sign == 1:
            t += 1
    return render(request, 'sign_index.html', {'event': event,'num':tt,'sign':t})


# 签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone','')
    a = Event.objects.filter(id=event_id)
    guest_list = Guest.objects.filter(event_id=a)
    p = Paginator(guest_list, 2)
    tt = p.count
    t = 0
    for guest in guest_list:
        if guest.sign == 1:
            t = t + 1
    result = Guest.objects.filter(phone = phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'phone error.','num':tt,'sign':t})
    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request, 'sign_index.html', {'event': event,'hint': 'event id or phone error.','num':tt,'sign':t})
    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event,'hint': "user has sign in.",'num':tt,'sign':t})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign = '1')
        t += 1
        return render(request, 'sign_index.html', {'event': event,'hint':'sign in success!','guest': result,'num':tt,'sign':t})


# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response