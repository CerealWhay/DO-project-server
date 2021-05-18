from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.Serializer):
    """Сериализатор пользователя."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    last_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class PersonSerializer(serializers.Serializer):
    """Сериализатор принадлежности к типу пользователя."""
    is_person = serializers.CharField(required=True)


class RegisterSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователя."""

    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirmation = serializers.CharField(required=True)
    first_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    last_name = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class LoginSerializer(serializers.Serializer):
    """Сериализатор авторизации пользователя."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class LoginResponseSerializer(serializers.Serializer):
    """Сериализатор ответа на авторизацию."""

    token = serializers.CharField()
    user = UserSerializer()
    person = serializers.CharField(required=True)


class ValidationErrorSerializer(serializers.Serializer):
    """Сериализатор ошибки валидации."""

    message = serializers.CharField(required=True, help_text='Текст ошибки')
    is_field_error = serializers.BooleanField(
        required=True, help_text='Относится ли ошибка к полю формы'
    )
    field = serializers.BooleanField(
        required=False, help_text='Название поля, к которому относится ошибка'
    )