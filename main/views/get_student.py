from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Student
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def get_student(request, student):
    student = Student.objects.get(id=student)
    setModel(student, request)
    return render(request, 'student.html', {"student": student})