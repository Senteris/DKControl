from datetime import date, timedelta
from main.views.functionsAndClasses.requestedData import RequestedData
from main.views.functionsAndClasses.statsMethods import *


def getAttending(req, daysQuantity):
    startday = date.today() - timedelta(days=daysQuantity-1)
    days = [startday + timedelta(days=s) for s in range(daysQuantity)]

    results = list()
    if req.user is None:
        for i in range(daysQuantity):
            results.append(getAttendingStats(days[i], days[i], req.union, req.group, req.student)[0])
    else:
        for i in range(daysQuantity):
            results.append(getAttendingTeacherStats(days[i], days[i], req.user)[0])

    i = 0
    for ii in range(daysQuantity):
        if results[i] == 0.001:
            days.pop(i)
            results.pop(i)
        else: i += 1


    return days, results
