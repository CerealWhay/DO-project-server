from django.db import models
from .logic.upload_step_directory import course_step_file_path


class Course(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    course_name = models.CharField(max_length=50)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name


class CourseStep(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE,)
    file = models.FileField(upload_to=course_step_file_path)

    def __str__(self):
        return self.file
