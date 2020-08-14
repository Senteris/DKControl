from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.models import User
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def theme(request):
    request.user.theme = request.GET.get('theme')
    request.user.save()
    return HttpResponse("OK")
