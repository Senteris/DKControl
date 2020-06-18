from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from main.models import Student


@login_required(login_url="/login/")
def removeStudent(request, student):
    student = Student.objects.get(id=student)
    student.delete()
    return redirect('/?operation=success')