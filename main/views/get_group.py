from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import *
from main.views.functionsAndClasses.statsMethods import getAttendingStats


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

    return render(request, 'group.html', {"group": group, "timetable": timetable, "attendings": attendings})