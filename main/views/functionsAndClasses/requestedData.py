from datetime import date


class RequestedData:
    #region Vars
    days = None
    unit = None
    periodStart = None
    periodEnd = None
    union = None
    group = None
    student = None
    user = None
    min = None
    max = None
    #endregion

    def __init__(self, request):
        self.days = request.GET.get('days', 30)
        self.unit = request.GET.get('unit', 'days')
        periodStart = request.GET.get('ps', None)
        periodEnd = request.GET.get('pe', None)
        union = request.GET.get('un', None)
        group = request.GET.get('g', None)
        student = request.GET.get('s', None)
        user = request.GET.get('us', None)
        min = request.GET.get('min', 0)
        max = request.GET.get('max', 100)

        if union is not None: self.union = int(union)
        if group is not None: self.group = int(group)
        if student is not None: self.student = int(student)
        if user is not None: self.user = int(user)
        self.min = int(min)
        self.max = int(max)

        if periodStart is not None: self.periodStart = date.strftime(periodStart, '%Y-%m-%d')
        if periodEnd is not None: self.periodEnd = date.strftime(periodEnd, '%Y-%m-%d')