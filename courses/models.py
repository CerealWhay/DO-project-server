from django.db import models
from .logic.upload_step_directory import course_step_file_path, student_answer_file_path


class Course(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    course_name = models.CharField(max_length=50)
    course_description = models.CharField(max_length=250)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name


class CourseStep(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE,)
    file = models.FileField(upload_to=course_step_file_path)

    def __str__(self):
        return str(self.file)

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()


class StudentAnswer(models.Model):
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE)
    file = models.FileField(upload_to=student_answer_file_path)
    step = models.ForeignKey(CourseStep, on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.file)

    def delete(self, using=None, keep_parents=False):
        self.file.storage.delete(self.file.name)
        super().delete()
