from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from .models import CourseStep, Course
from users.models import Teacher
from .serializers import UploadStepSerializer, CreateCourseSerializer


class UploadViewSet(ViewSet):

    @action(methods=('post',), detail=False)
    def create_course(self, request):
        serializer = CreateCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_name = serializer.validated_data.get('course_name')

        course = Course(
            course_name=course_name,
            teacher=Teacher.objects.filter(user=user).first(),
        )
        course.save()

        response = "POST API and you have created a {} course".format(course_name)
        return Response(response)

    @action(methods=('post',), detail=False)
    def create_step(self, request):
        print(request.user)
        serializer = UploadStepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data.get('file')
        course = serializer.validated_data.get('course')

        step = CourseStep(
            file=file,
            course=Course.objects.filter(course_name=course).first(),
        )
        step.save()

        response = "POST API and you have uploaded a {} file".format(file)
        return Response(response)

