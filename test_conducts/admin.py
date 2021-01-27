from django.contrib import admin
from .models import StudentTests, Conduct


class StudentTestAdmin(admin.ModelAdmin):
    readonly_fields = ('test_id', 'date')


admin.site.register(StudentTests, StudentTestAdmin)
admin.site.register(Conduct)
