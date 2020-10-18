import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q, CharField, DateTimeField
from django.db.models import Value as V
from django.db.models.functions import *
from django.http import JsonResponse
from django.shortcuts import render

from main.models import *


@login_required(login_url="/login/")
def search(request):
    query = request.GET.get('q')
    is_json = request.GET.get('json')

    if is_json is None:
        return render(request, 'search.html')
    elif len(query) == 0 and is_json != "extend":
        return JsonResponse({"results": {"additions": {
            "name": "Дополнительно",
            "results": [
                {"title": f"Расширинный поиск", "description": 'Поиск с фильтрами', "url": "/search/"}]
        }}})
    else:
        query = query.split()

        students = Student.objects.annotate(full_name=Concat('last_name', V(' '), 'first_name', V(' '), 'patronymic')) \
            .filter(Q(is_archived=False))
        teachers = Employee.objects.annotate(full_name=Concat('last_name', V(' '), 'first_name', V(' '), 'patronymic')) \
            .filter(Q(is_archived=False))
            # .filter(Q(groups__name='Педагог', is_archived=False))
        parents = Parent.objects.annotate(full_name=Concat('last_name', V(' '), 'first_name', V(' '), 'patronymic'))

        groups = Group.objects.annotate(full_name=Concat('union__name', V(' '), 'name'))
        study_sessions = StudySession.objects.all()

        if is_json == "extend":
            filters = request.GET.get('filters')
            if filters is not None:
                filters = filters.split(',')
                filters = list({'students', 'teachers', 'parents', 'groups', 'sessions'} - set(filters))
                if len(filters) != 5 or len(query) == 0:
                    if "students" in filters:
                        students = students.none()
                    if "teachers" in filters:
                        teachers = teachers.none()
                    if "parents" in filters:
                        parents = parents.none()
                    if "groups" in filters:
                        groups = groups.none()
                    if "sessions" in filters:
                        study_sessions = study_sessions.none()

            age_range = request.GET.get('age')
            if age_range is not None:
                age_range = age_range.split('-')
                for i, age in enumerate(age_range):
                    age_range[i] = date.today() - relativedelta(years=int(age))
                students = students.filter(birthday__range=[age_range[1], age_range[0]])

            date_start = request.GET.get('start')
            date_end = request.GET.get('end')
            if date_start is not None and date_end is not None:
                if date_start == '': date_start = datetime.datetime(2000, 1, 1)
                if date_end == '': date_end = datetime.datetime.now()
                study_sessions = study_sessions.filter(date__range=[date_start, date_end])

        for query in query:
            students = students.filter(Q(full_name__icontains=query))
            teachers = teachers.filter(Q(full_name__icontains=query))
            parents = parents.filter(Q(full_name__icontains=query))
            groups = groups.filter(Q(full_name__icontains=query))
            study_sessions = [s for s in study_sessions if
                              query in s.date.strftime("%d.%m.%Y %H:%M:%S") or query in s.group.__str__()]

        return JsonResponse({"results": {
            "students": {
                "name": "Ученики",
                "results": [{"title": f"{s.last_name} {s.first_name} {s.patronymic}",
                             "description": f"{', '.join([g.__str__() for g in s.groups.all()])}",
                             "url": f"/students/{s.id}/",
                             "extend": [{"name": g.__str__(), "url": f"/groups/{g.id}/"} for g in s.more.groups.all()]} for s in students],
            },
            "teachers": {
                "name": "Педагоги",
                "results": [
                    {"title": f"{s.last_name} {s.first_name} {s.patronymic}",
                     "description": f"{', '.join([g.__str__() for g in s.group_set.all()])}",
                     "url": f"/users/{s.id}/",
                     "extend": [{"name": g.__str__(), "url": f"/groups/{g.id}/"} for g in s.group_set.all()]} for s in teachers]
            },
            "parents": {
                "name": "Родители",
                "results": [
                    {"title": f"{s.last_name} {s.first_name} {s.patronymic}",
                     "description": f"{', '.join([c.__str__() for c in s.childs.all()])}",
                     "url": f"/parents/{s.id}/",
                     "extend": [{"name": c.user.__str__(), "url": f"/students/{c.user.id}/"} for c in s.childs.all()]} for s in parents]
            },
            "groups": {
                "name": "Группы",
                "results": [
                    {"title": f"{s.name} {s.union.name}",
                     "description": f"{', '.join([t.__str__() for t in s.timetableelem_set.all()])}",
                     "url": f"/groups/{s.id}/",
                     "extend": [{"name": g.__str__(), "url": f"/students/{g.id}/"} for g in s.students.all()]} for s in groups]
            },
            "sessions": {
                "name": "Занятия",
                "results": [
                    {"title": f"{s.group} {s.date.strftime('%d.%m.%Y %H:%M:%S')}",
                     "description": f"{s.group}",
                     "url": f"/sessions/{s.id}/",
                     "extend": [{"name": s.group.__str__(), "url": f"/sessions/{s.id}/"}]} for s in study_sessions]
            },
            "additions": {
                "name": "Дополнительно",
                "results": [
                    {"title": f"Расширинный поиск", "description": 'Поиск с фильтрами', "url": "/search/"}]
            },
        }})
