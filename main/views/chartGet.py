from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.views.functionsAndClasses.chartMethods import *
from main.views.functionsAndClasses.requestedData import RequestedData
from main.views.functionsAndClasses.statsMethods import *


@login_required(login_url="/login/")
def chartGet(request, chartType):
    req = RequestedData(request)


    if chartType == 'attendingStats' and req.unit == 'days':
        days, results = getAttending(req, req.days)

        return JsonResponse({
            "region": [d.day for d in days],
            "value": [int(round(result*100)) for result in results]
        })

    if chartType == 'attendingStats' and req.unit == 'months':
        if date.today().month >= 9: editYear = 0
        else: editYear = 1
        startday = date(date.today().year - editYear, 9, 1)

        periodsStart = [startday + relativedelta(months=s) for s in range(9)] #Get dates all month
        periodsEnd = [startday + relativedelta(months=s+1) for s in range(9)] #Get dates end all month

        if req.user is None: results = [getAttendingStats(periodsStart[i], periodsEnd[i], req.union, req.group, req.student) for i in range(9)]
        else:                results = [getAttendingTeacherStats(periodsStart[i], periodsEnd[i], req.user) for i in range(9)]

        return JsonResponse({
            "region": ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май"],
            "value": [int(round(result[0]*100)) for result in results]
        })