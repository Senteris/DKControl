from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import *


@login_required(login_url="/login/")
def getUser(request, user):
    user = User.objects.get(id=user)
    return render(request, 'user.html', {"user": user})