from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from  main.models import *

admin.site.register(Group)
admin.site.register(Timetable)
admin.site.register(Union)
admin.site.register(ElemOfTimetable)
admin.site.register(Parent)
admin.site.register(Student)

class CustomUserAdmin(UserAdmin):
    # as an example, this custom user admin orders users by email address
    ordering = ('email',)

    fieldsets = (
        ('Персональная информация', {
             'fields': ('first_name', 'last_name', 'patronymic')
        }),
    )

admin.site.register(User, CustomUserAdmin)
