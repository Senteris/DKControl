from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from main.models import User
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def newStudent(request, student):
    user = User.objects.get(id=student)
    setModel(user, request)
    return render(request, 'user.html', {"user": user})