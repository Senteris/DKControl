from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import *


@login_required(login_url="/login/")
def get_parent(request, parent):
    parent = Parent.objects.get(id=parent)
    return render(request, 'parent.html', {'parent': parent})