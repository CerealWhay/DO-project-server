from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CourseStep, Course
from users.logic.user_info import get_teacher
from .serializers import (
    CreateStepSerializer,
    CreateCourseSerializer,
    CourseSerializer,
    StepSerializer,
)


class CoursesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('get',), detail=False)
    def get_courses_as_teacher(self, request):
        courses = Course.objects.filter(teacher=get_teacher(request.user))

        response = []
        for course in courses:
            serializer = CourseSerializer(
                data=dict(
                    # id курса
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

        courses = Course.objects.filter(teacher=get_teacher(request.user))
        course = courses.filter(
            course_name=serializer.validated_data.get('course_name'),
            id=serializer.validated_data.get('id'),
            course_description=serializer.validated_data.get('course_description'),
            date=serializer.validated_data.get('date'),
        ).first()
        response = 'course not found'
        if course:
            response = f'course {course} deleted'
            course.delete()

        return Response(
            data=response, status=status.HTTP_200_OK
        )


class StepsViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=('post',), detail=False)
    def get_steps_as_teacher(self, request):
        courses = Course.objects.filter(teacher=get_teacher(request.user))
        course = courses.filter(
            id=request.data.get('id'),
        ).first()
        steps = CourseStep.objects.filter(course=course)
        response = []
        for step in steps:
            upload_serializer = StepSerializer(
                data=dict(
                    id=step.id,
                    file_name=step.file.url,
                )
            )
            upload_serializer.is_valid(raise_exception=True)
            response.append(upload_serializer.validated_data)
        return Response(
            data=response, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def create_step(self, request):
        serializer = CreateStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        courses = Course.objects.filter(teacher=get_teacher(request.user))

        course = courses.filter(
            # id курса
            id=serializer.validated_data.get('id'),
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
        ).first()
        response = 'step not found'
        if step:
            response = f'step {step} deleted'
            step.delete()

        return Response(
            data=response, status=status.HTTP_200_OK
        )
