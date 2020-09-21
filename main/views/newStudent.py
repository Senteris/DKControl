from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from decorators import employee_required
from main.models import Student


@login_required(login_url="/login/")
@employee_required()
def newStudent(request):
    student = Student()
    student.save()
    return redirect('/students/'+ str(student.id) + "?edit=True")