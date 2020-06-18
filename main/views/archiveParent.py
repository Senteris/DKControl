from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from main.models import User


@login_required(login_url="/login/")
def archiveParent(request, parent):
    parent = User.objects.get(id=parent)
    parent.isArchived = True
    parent.save()
    return redirect('/?operation=success')