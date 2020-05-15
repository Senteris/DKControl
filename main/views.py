from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, CharField
from django.db.models import Value as V
from django.db.models.functions import Concat, Cast, ExtractHour, ExtractMinute, TruncMinute, TruncHour
from django.http import JsonResponse
from django.shortcuts import render, redirect

from main.models import *


@login_required(login_url="/login/")
def main(request):
    students = Student.objects.all()[:20]
    # region students attending
    if date.today().month >= 9:
        editYear = 0
    else:
        editYear = 1

    startday = date(date.today().year - editYear, 9, 1)
    periodEnd = startday + relativedelta(months=10)
    attendings = [round(getAttendingStats(startday, periodEnd, None, None, student.id)[0] * 100) for student in students]
    # endregion
    return render(request, 'main.html', {'students': students, 'attendings': attendings})


def login(request):
    error = None
    if request.user.is_authenticated:
        return redirect('main')
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
                    return redirect('main')
            else:
                error = "  Имя или пароль неверны"
        else:
            # the authentication system was unable to verify the username and password
            error = "  Имя или пароль неверны"
    return render(request, "login.html", {'error': error})


def logout(request):
    user_logout(request)
    return redirect('login')


@login_required(login_url="/login/")
def search(request):
    query = request.GET.get('q')
    if query is None:
        return render(request, 'main.html')
    elif len(query) == 0:
        return JsonResponse({})
    else:
        query = query.split()

        students = Student.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' '), 'patronymic')) \
            .filter(Q(isDeleted=False))
        teachers = User.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' '), 'patronymic')) \
            .filter(Q(groups__name='Педагог'))
        parents = Parent.objects.annotate(full_name=Concat('first_name', V(' '), 'last_name', V(' '), 'patronymic'))

        groups = Group.objects.annotate(full_name=Concat('union__name', V(' '), 'name'))
        timetable_elems = TimetableElem.objects.annotate(
            beginTimeStr=Cast(TruncMinute('beginTime'), CharField()),
            endTimeStr=Cast(TruncMinute('endTime'), CharField()),
            timeStr=Concat('beginTimeStr', V('-'), 'endTimeStr')
        )

        for query in query:
            students = students.filter(Q(full_name__icontains=query))
            teachers = teachers.filter(Q(full_name__icontains=query))
            parents = parents.filter(Q(full_name__icontains=query))
            groups = groups.filter(Q(full_name__icontains=query))
            timetable_elems = timetable_elems.filter(Q(timeStr__icontains=query))

        return JsonResponse({"results": {
            "students": {
                "name": "Ученики",
                "results": [{"title": f"{s.first_name} {s.last_name} {s.patronymic}", "description": "",
                             "url": f"/students/{s.id}/"} for s in students]
            },
            "teachers": {
                "name": "Учителя",
                "results": [
                    {"title": f"{s.first_name} {s.last_name} {s.patronymic}", "description": ""} for s in teachers]
            },
            "parents": {
                "name": "Родители",
                "results": [
                    {"title": f"{s.first_name} {s.last_name} {s.patronymic}", "description": ""} for s in parents]
            },
            "groups": {
                "name": "Группы",
                "results": [
                    {"title": f"{s.name} {s.union.name}", "description": "", "url": f"/groups/{s.id}/"} for s in groups]
            },
            "timetable_elems": {
                "name": "Время",
                "results": [
                    {"title": f"{s.timeStr}", "description": ""} for s in timetable_elems]
            },
        }})


@login_required(login_url="/login/")
def chartGet(request, chartType):
    if date.today().month >= 9: editYear = 0
    else: editYear = 1

    startday = date(date.today().year - editYear, 9, 1)

    #region GetData
    periodStart = request.GET.get('ps', None)
    periodEnd = request.GET.get('pe', None)
    union = request.GET.get('u', None)
    group = request.GET.get('g', None)
    student = request.GET.get('s', None)
    min = request.GET.get('min', 0)
    max = request.GET.get('max', 100)

    if union is not None: union = int(union)
    if group is not None: group = int(group)
    if student is not None: student = int(student)
    min = int(min)
    max = int(max)

    if periodStart is not None: periodStart = date.strftime(periodStart, '%Y-%m-%d')
    if periodEnd is not None: periodEnd = date.strftime(periodEnd, '%Y-%m-%d')
    #endregion

    if chartType == 'chartStudent':

        periodsStart = [startday + relativedelta(months=s) for s in range(9)] # :(
        periodsEnd = [startday + relativedelta(months=s+1) for s in range(9)]

        results = [getAttendingStats(periodsStart[i], periodsEnd[i], None, group, student) for i in range(9)]

        return JsonResponse({
            "region": ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май"],
            "value": [result[0]*100 for result in results]
        })

#region Methods
def getAttendingStats(periodStart, periodEnd, union, group, student):
    allAttendings = [a
                     for a in Attending.objects.all()
                     if a.studySession.date.date() >= periodStart
                     and a.studySession.date.date() <= periodEnd
                     and (union is None or a.studySession.group.union.id == int(union))
                     and (group is None or a.studySession.group.id == int(group))
                     and (student is None or a.student.id == int(student))
                     ]

    attendedAttendings = [a
                          for a in allAttendings
                          if a.isAttend==True]

    if len(allAttendings) == 0: allAttendings = 1;
    else: allAttendings = len(allAttendings)
    return len(attendedAttendings) / allAttendings, len(attendedAttendings), allAttendings

def getGenderStats(union, group):
    allStudents = getAllStudents(union, group)
    maleStudents = [m
                    for m in allStudents
                    if m.gender == "Мужской"]

    return len(maleStudents) / len(allStudents), len(maleStudents), len(allStudents)

def getAgeStats(min, max, union, group):
    allStudents = getAllStudents(union, group)
    chosenStudents = [m
                      for m in allStudents
                      if m.age >= min
                      and m.age <= max]

    return len(chosenStudents) / len(allStudents), len(chosenStudents), len(allStudents)
#endregion

#region Methods for other methods
def getAllStudents(union, group):
    return [s
            for s in Student.objects.all()
            if (union is None or s.group.union.id == int(union))
            and (group is None or s.group.id == int(group))
            ]
#endregion


@login_required(login_url="/login/")
def get_student(request, student):
    student = Student.objects.get(id=student)
    return render(request, 'student_profile.html', {"student": student})


@login_required(login_url="/login/")
def get_group(request, group):
    group = Group.objects.get(id=group)
    timetable = {
        "ПН": {},
        "ВТ": {},
        "СР": {},
        "ЧТ": {},
        "ПТ": {},
        "СБ": {},
    }

    for time in group.timetableelem_set.all():
        timetable[time.day] = {"time": f"{time.beginTime.strftime('%H:%M')}-{time.endTime.strftime('%H:%M')}"}

    # region students attending
    if date.today().month >= 9: editYear = 0
    else: editYear = 1

    startday = date(date.today().year - editYear, 9, 1)

    periodEnd = startday + relativedelta(months=10)

    attendings = [round(getAttendingStats(startday, periodEnd, None, group.id, student.id)[0] * 100) for i, student in enumerate(group.students.all())]
    # endregion

    return render(request, 'group_view.html', {"group": group, "timetable": timetable, "attendings": attendings})


@login_required(login_url="/login/")
def get_parent(request, parent):
    parent = Parent.objects.get(id=parent)
    return render(request, 'parent_profile.html', {'parent': parent})
