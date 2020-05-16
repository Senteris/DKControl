from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.views.functions.statsMethods import getAttendingStats


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

    if chartType == 'attendingStats12m':

        periodsStart = [startday + relativedelta(months=s) for s in range(9)] # :(
        periodsEnd = [startday + relativedelta(months=s+1) for s in range(9)]

        results = [getAttendingStats(periodsStart[i], periodsEnd[i], None, group, student) for i in range(9)]

        return JsonResponse({
            "region": ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь", "Февраль", "Март", "Апрель", "Май"],
            "value": [result[0]*100 for result in results]
        })