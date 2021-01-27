from .models import Parent, Teacher, Student
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .customuser import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'Professional Info', {'fields': ('user_type',)}
        )
    )


class TeacherAdmin(admin.ModelAdmin):
    readonly_fields = ('teacher_id',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
