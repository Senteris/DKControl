from django.http import JsonResponse

from main.models import Attending


def set_attending(request, attending):
    attending = Attending.objects.get(id=attending)
    attending.isAttend = bool(request.GET.get("status"))
    attending.save()
    return JsonResponse({})
