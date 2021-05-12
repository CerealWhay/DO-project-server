from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField('first name', max_length=150, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)

    class Meta:
        abstract = True


class Teacher(Person):
    is_teacher = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Student(Person):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
