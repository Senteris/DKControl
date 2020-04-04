from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, CharField
from django.db.models import Value as V
from django.db.models.functions import Concat, Cast, ExtractHour, ExtractMinute
from django.http import JsonResponse
from django.shortcuts import render, redirect

from main.models import Student, User, Parent, Union, Group, TimetableElem


@login_required(login_url="login/")
def index(request):
    return render(request, 'index.html', {})

def login(request):
    error = None
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User '{}' is valid, active and authenticated".format(user.username))
                user_login(request, user)

                if request.GET.get('next', None) is not None:
                    return redirect(request.GET['next'])
                else:
                    return redirect('index')
            else:
                error = "  Имя или пароль неверны"
        else:
            # the authentication system was unable to verify the username and password
            error = "  Имя или пароль неверны"
    return render(request, "login.html", {'error': error})

def logout(request):
    user_logout(request)
    return redirect('index')


@login_required(login_url="login/")
def search(request):
    query = request.GET.get('q')
    if query is None:
        return render(request, 'index.html')
    elif len(query) == 0:
        return JsonResponse({})
    else:
        students = Student.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' '), 'patronymic')).filter(
            Q(full_name__icontains=query) & Q(isDeleted=False)
        )
        teachers = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' '), 'patronymic')).filter(
            Q(full_name__icontains=query) & Q(groups__name='Педагог')
        )
        parents = Parent.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' '), 'patronymic')).filter(
            Q(full_name__icontains=query)
        )
        groups = Group.objects.annotate(full_name=Concat('union__name', V(' '), 'name'), full_name_reverce=Concat('name', V(' '), 'union__name')).filter(
            Q(full_name__icontains=query) | Q(full_name_reverce__icontains=query)
        )
        timetable_elems = TimetableElem.objects.annotate(
            hour=Cast(ExtractHour('beginTime'), CharField()),
            minute=Cast(ExtractMinute('beginTime'), CharField()),
            beginTimeStr=Concat(
                'hour', V(':'), 'minute',
                output_field=CharField()
            )
        ).filter(
            Q(beginTimeStr__startswith=query)
        )
        return JsonResponse({'students': [f"{s.first_name} {s.last_name} {s.patronymic}" for s in students],
                             'parents': [f"{s.first_name} {s.last_name} {s.patronymic}" for s in parents],
                             'teachers': [f"{s.first_name} {s.last_name} {s.patronymic}" for s in teachers],
                             'groups': [f"{s.name} {s.union.name}" for s in groups],
                             'timetable_elems': [f"{s.beginTimeStr}" for s in timetable_elems]})

