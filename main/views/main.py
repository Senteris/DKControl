from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import *
from main.views.functionsAndClasses.statsMethods import getAttendingStats


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
    return render(request, 'unions.html', {'students': students, 'attendings': attendings, 'unions': Union.objects.all()})