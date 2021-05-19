from rest_framework import serializers


# Serializers define the API representation.
class UploadStepSerializer(serializers.Serializer):
    file = serializers.FileField()
    course = serializers.CharField()


class CreateCourseSerializer(serializers.Serializer):
    course_name = serializers.CharField()
