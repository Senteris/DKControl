from main.models import *


def setModel(model, request):
    if len(request.GET) != 0:
        for name, value in request.GET.items():
            if name == 'fio':
                continue

            attr = None
            name = name.split('.')
            if len(name) > 1:
                attr = getattr(model, name.pop(0))
                for name_sp in name[:-1]:
                    attr = getattr(attr, name_sp)

                setattr(attr, name[-1], value)
                attr.save()
            else:
                setattr(model, name[-1], value)

        if request.GET.get('fio') is not None:
            last_name, first_name, patronymic = request.GET.get('fio').split(' ')
            setattr(model, 'last_name', last_name)
            setattr(model, 'first_name', first_name)
            setattr(model, 'patronymic', patronymic)
        model.save()
        return True
    else:
        return False
