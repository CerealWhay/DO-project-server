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
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Student(Person):
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
