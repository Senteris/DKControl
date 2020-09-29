from django.urls import path
from reports.views import report_generate, reports

urlpatterns = [
    path("", reports, name="reports"),
    path("<str:report_type>/generate/", report_generate, name="report_generate"),
]
