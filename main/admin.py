from django.contrib import admin
from django.contrib import admin
from .models import Student, Group


class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'group', 'chosen_grade', 'registration_date', 'grade_choice_date', 'assigned_tasks')


admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
