from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Union


@login_required(login_url="/login/")
def getUnion(request, union):
    union = Union.objects.get(id=union)
    return render(request, 'union.html', {"union": union})