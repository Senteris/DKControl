from django.contrib.auth.decorators import login_required
from django.db.models import Q, CharField
from django.db.models import Value as V
from django.db.models.functions import Concat, Cast, TruncMinute
from django.http import JsonResponse
from django.shortcuts import render

from main.models import *


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