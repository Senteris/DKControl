from django.http import Http404, JsonResponse
from django.shortcuts import render
from reports.reports import Report

reports_list = Report.__subclasses__()


def get_report(report_type):
    for r in reports_list:
        if r.id == report_type:
            return r
    raise Http404("Запрашиваемый отсчёт не найден")


def reports(request):
    return render(request, 'reports.html')


def report_generate(request, report_type):
    return JsonResponse(get_report(report_type)(request.GET).generate())

