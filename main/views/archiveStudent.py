from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from main.models import Student


@login_required(login_url="/login/")
def archiveStudent(request, student):
    student = Student.objects.get(id=student)
    student.isArchived = True
    student.save()
    return redirect('/?operation=success')