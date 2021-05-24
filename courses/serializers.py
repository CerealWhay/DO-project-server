from rest_framework import serializers


# Serializers define the API representation.
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    course_name = serializers.CharField(required=True)
    course_description = serializers.CharField(required=True, max_length=250)
    date = serializers.DateTimeField(required=True)


class CreateCourseSerializer(serializers.Serializer):
    course_name = serializers.CharField(required=True)
    course_description = serializers.CharField(required=True)


class StepSerializer(serializers.Serializer):
    file_name = serializers.CharField(required=False)
    id = serializers.IntegerField(required=True)


class CreateStepSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    id = serializers.IntegerField(required=True)
