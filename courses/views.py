from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import Teacher, Student
from .models import CourseStep, Course, StudentAnswer
from users.logic.user_info import get_teacher, get_student
from .serializers import (
    CreateStepSerializer,
    CreateCourseSerializer,
    CourseSerializer,
    StepSerializer,
    AnswerSerializer,
    StudentSerializer,
)


class AllCoursesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('get',), detail=False)
    def get_all_courses(self, request):
        courses = Course.objects.all()
        response = []
        for course in courses:
            teacher = course.teacher
            serializer = CourseSerializer(
                data=dict(
                    teacher_firstname=teacher.user.first_name,
                    teacher_lastname=teacher.user.last_name,
                    id=course.id,
                    course_name=course.course_name,
                    course_description=course.course_description,
                    date=course.date,
                )
            )
            serializer.is_valid(raise_exception=True)
            response.append(serializer.validated_data)
        return Response(
            data=response, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def get_steps(self, request):
        steps = CourseStep.objects.filter(
            course__id=request.data.get('id'),
        )
        serializer = StepSerializer(steps, many=True)
        response = serializer.data
        return Response(
            data=response, status=status.HTTP_200_OK
        )


class TeacherCoursesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('get',), detail=False)
    def get_courses_as_teacher(self, request):
        courses = Course.objects.filter(teacher=get_teacher(request.user))
        serializer = CourseSerializer(courses, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def create_course(self, request):
        serializer = CreateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_name = serializer.validated_data.get('course_name')
        course_description = serializer.validated_data.get('course_description')
        course = Course(
            course_name=course_name,
            teacher=get_teacher(request.user),
            course_description=course_description,
        )
        course.save()

        response = "POST API and you have created a {} course".format(course_name)
        return Response(response)

    @action(methods=('post',), detail=False)
    def delete_course(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = Course.objects.filter(
            id=serializer.validated_data.get('id'),
            teacher=get_teacher(request.user)
        ).first()
        response = 'course not found'
        if course:
            response = f'course {course} deleted'
            course.delete()

        return Response(
            data=response, status=status.HTTP_200_OK
        )

    @action(methods=('get',), detail=False)
    def get_students(self, request):
        courses = Course.objects.filter(teacher=get_teacher(request.user))
        students = set()
        for course in courses:
            student = course.student_set.all()
            if student:
                students.add(student.first())

        response = []
        for student in students:
            serializer = StudentSerializer(
                data=dict(
                    student_firstname=student.user.first_name,
                    student_lastname=student.user.last_name,
                    id=student.id,
                )
            )
            serializer.is_valid(raise_exception=True)
            response.append(serializer.validated_data)

        return Response(
            data=response, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def get_courses_by_student(self, request):

        student = Student.objects.filter(id=request.data.get('id'),)
        courses = student.first().courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def make_answer_done(self, request):
        answer = StudentAnswer.objects.filter(id=request.data.get('id')).first()
        answer.is_done = True
        answer.save()
        response = f'answer {answer} is done now.'

        return Response(
            data=response, status=status.HTTP_200_OK
        )


class TeacherStepsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('post',), detail=False)
    def create_step(self, request):
        serializer = CreateStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course = Course.objects.filter(
            id=serializer.validated_data.get('id'),
            teacher=get_teacher(request.user)
        ).first()

        step = CourseStep(
            file=serializer.validated_data.get('file'),
            course=course,
        )
        step.save()

        response = "POST API and you have uploaded a file"
        return Response(response)

    @action(methods=('post',), detail=False)
    def delete_step(self, request):
        serializer = StepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        step = CourseStep.objects.filter(
            # id шага
            id=serializer.validated_data.get('id'),
            course__teacher=get_teacher(request.user)
        ).first()
        response = 'step not found'
        if step:
            response = f'step {step} deleted'
            step.delete()

        return Response(
            data=response, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def get_answers(self, request):
        student = Student.objects.filter(id=request.data.get('student_id')).first()
        courses_id = request.data.get('courses_id').split(',')
        courses = []
        for course_id in courses_id:
            tmp = Course.objects.filter(id=course_id).first()
            courses.append(tmp)

        full_answers = []
        for course in courses:
            answers = StudentAnswer.objects.filter(
                student=student,
                step__course=course
            )
            serializer = AnswerSerializer(answers, many=True)
            full_answers.append(
                dict(
                    course=course.id,
                    data=serializer.data
                )
            )
        return Response(
            data=full_answers, status=status.HTTP_200_OK
        )


class StudentCoursesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('get',), detail=False)
    def get_courses_as_student(self, request):
        courses = Course.objects.filter(student=get_student(request.user))
        serializer = CourseSerializer(courses, many=True)
        return Response(
            data=serializer.data, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def subscribe_course(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = get_student(request.user)

        course = Course.objects.filter(
            id=serializer.validated_data.get('id'),
        ).first()
        student.courses.add(course)

        print(course.student_set.all())
        response = f'student {student} has subscribed on {course} course.'

        return Response(
            data=response, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def unsubscribe_course(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = get_student(request.user)

        course = Course.objects.filter(
            id=serializer.validated_data.get('id'),
        ).first()
        student.courses.remove(course)

        response = f'student {student} has unsubscribed on {course} course.'

        return Response(
            data=response, status=status.HTTP_200_OK
        )


class StudentStepsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('post',), detail=False)
    def create_answer(self, request):
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        step = CourseStep.objects.filter(
            id=serializer.validated_data.get('step'),
        ).first()

        answer = StudentAnswer(
            file=serializer.validated_data.get('file'),
            student=get_student(request.user),
            step=step,
        )
        answer.save()

        response = "POST API and you have uploaded a file (answer)"
        return Response(response)

    @action(methods=('post',), detail=False)
    def get_answers(self, request):
        courses_id = request.data.get('courses_id').split(',')
        courses = []
        for course_id in courses_id:
            tmp = Course.objects.filter(id=course_id).first()
            courses.append(tmp)

        full_answers = []
        for course in courses:
            answers = StudentAnswer.objects.filter(
                student=get_student(request.user),
                step__course=course
            )
            serializer = AnswerSerializer(answers, many=True)
            full_answers.append(
                dict(
                    course=course.id,
                    data=serializer.data
                )
            )
        return Response(
            data=full_answers, status=status.HTTP_200_OK
        )