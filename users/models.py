from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        abstract = True


class Teacher(Person):
    pass


class Student(Person):
    pass
