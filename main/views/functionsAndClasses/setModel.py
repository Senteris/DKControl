from main.models import *

def setModel(model, request):
    for name, value in request.GET.items():
        setattr(model, name, value)
    model.save()