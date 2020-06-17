from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from main.models import User


@login_required(login_url="/login/")
def removeUser(request, user):
    user = User.objects.get(id=user)
    user.delete()
    return redirect('main')