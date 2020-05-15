from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import *


@login_required(login_url="/login/")
def get_student(request, student):
    student = Student.objects.get(id=student)
    return render(request, 'student_profile.html', {"student": student})