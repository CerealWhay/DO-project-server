from ..models import Teacher, Student

TEACHER_ROLE = 'teacher'
STUDENT_ROLE = 'student'
ADMIN = 'admin'


def define_role(user):
    if Teacher.objects.filter(user=user).exists():
        return TEACHER_ROLE
    elif Student.objects.filter(user=user).exists():
        return STUDENT_ROLE
    else:
        return ADMIN
