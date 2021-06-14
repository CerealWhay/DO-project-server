from rest_framework import serializers


# Serializers define the API representation.
class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    course_name = serializers.CharField(required=True)
    course_description = serializers.CharField(required=True, max_length=250)
    date = serializers.DateTimeField(required=True)
    teacher = serializers.SlugRelatedField(slug_field='id', required=False, read_only=True)
    teacher_firstname = serializers.CharField(required=False)
    teacher_lastname = serializers.CharField(required=False)


class CreateCourseSerializer(serializers.Serializer):
    course_name = serializers.CharField(required=True)
    course_description = serializers.CharField(required=True)


class StepSerializer(serializers.Serializer):
    file = serializers.CharField(required=False)
    id = serializers.IntegerField(required=True)


class CreateStepSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    id = serializers.IntegerField(required=True)


class AnswerSerializer(serializers.Serializer):
    student = serializers.SlugRelatedField(slug_field='id', required=False, read_only=True)
    file = serializers.FileField(required=False)
    step = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    is_done = serializers.BooleanField(required=False)


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    student_firstname = serializers.CharField(required=False)
    student_lastname = serializers.CharField(required=False)
