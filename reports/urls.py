from django.urls import path
from reports.views import report_generate, reports, report_form

urlpatterns = [
    path("", reports, name="reports"),
    path("<str:report_type>/generate/", report_generate, name="report_generate"),
    path("<str:report_type>/form/", report_form, name="report_form"),
]
