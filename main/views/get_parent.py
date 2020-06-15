from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Parent
from main.views.functionsAndClasses.setModel import setModel


@login_required(login_url="/login/")
def get_parent(request, parent):
    parent = Parent.objects.get(id=parent)
    setModel(parent, request)
    return render(request, 'parent.html', {'parent': parent})