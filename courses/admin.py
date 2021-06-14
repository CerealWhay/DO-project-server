from django.contrib import admin

from .models import Course, CourseStep, StudentAnswer


admin.site.register(Course)
admin.site.register(CourseStep)

admin.site.register(StudentAnswer)
