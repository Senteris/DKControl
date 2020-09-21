from django.contrib.auth.decorators import user_passes_test
from main.models import User


def employee_required():
    return user_passes_test(
        lambda u: u.type == User.Types.EMPLOYEE
    )
