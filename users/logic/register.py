from django.contrib.auth import get_user_model

from .validation import UserDataValidator
from ..models import Teacher, Student

User = get_user_model()


class Registerer:
    """Класс-регистратор.

    Реализует поведение регистрации пользователя, включая валидацию.
    """

    @classmethod
    def _validate_data(cls, user_data: dict) -> None:
        """Валидирует регистрационные данные.

        Вызывает ValidationError в случае невалидных данных.
        """
        UserDataValidator.compare_passwords(
            user_data.get('password'),
            user_data.get('password_confirmation')
        )
        UserDataValidator.validate_username(user_data.get('username'))
        UserDataValidator.validate_email(user_data.get('email'))

    @classmethod
    def register_teacher(cls, user_data: dict) -> None:
        """Метод создания учителя."""
        user = cls._create_user(user_data)
        teacher = Teacher(user=user)
        teacher.save()

    @classmethod
    def register_student(cls, user_data: dict) -> None:
        """Метод создания ученика."""
        user = cls._create_user(user_data)
        student = Student(user=user)
        student.save()

    @classmethod
    def _create_user(cls, user_data: dict) -> User:
        """Регистрация пользователя."""
        cls._validate_data(user_data)
        user_data.pop('password_confirmation')
        user_password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(user_password)
        user.save()
        return user

