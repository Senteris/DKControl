from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import *

admin.site.register(Note)
admin.site.register(StudySession)
admin.site.register(Attending)
admin.site.register(Union)
admin.site.register(Group)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Logo)


class CustomUserAdmin(UserAdmin):
    # as an example, this custom user admin orders users by email address
    ordering = ('email',)

    fieldsets = (
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'patronymic', 'groups')
        }),
    )


@admin.register(TimetableElem)
class TimetableElemAdmin(admin.ModelAdmin):
    fields = ('beginTime', 'day', 'group')


admin.site.register(User, CustomUserAdmin)
