from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from main.models import Student


@login_required(login_url="/login/")
def newStudent(request):
    student = Student()
    student.save()
    return redirect('/students/'+ str(student.id) + "?edit=True")