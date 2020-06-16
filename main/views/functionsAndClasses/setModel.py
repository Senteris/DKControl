from main.models import *


def setModel(model, request):
    if len(request.GET) != 0:
        for name, value in request.GET.items():
            setattr(model, name, value)
        if request.GET.get('fio') is not None:
            last_name, first_name, patronymic = request.GET.get('fio').split(' ')
            setattr(model, 'last_name', last_name)
            setattr(model, 'first_name', first_name)
            setattr(model, 'patronymic', patronymic)
        model.save()
        return True
    else:
        return False
