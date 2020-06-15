from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import User
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def getUser(request, user):
    user = User.objects.get(id=user)
    setModel(user, request)
    return render(request, 'user.html', {"user": user})