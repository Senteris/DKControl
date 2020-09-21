from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from decorators import employee_required
from main.models import Parent


@login_required(login_url="/login/")
@employee_required()
def newParent(request):
    parent = Parent()
    parent.save()
    redirect('/parent/' + str(parent.id) + "?edit=True")