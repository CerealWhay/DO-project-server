from django.contrib.auth import get_user_model

from .validation import UserDataValidator

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
    def register(cls, user_data: dict) -> None:
        """Основной метод."""
        cls._validate_data(user_data)
        user_data.pop('password_confirmation')
        cls._perform_registration(user_data)

    @classmethod
    def _perform_registration(cls, user_data: dict) -> None:
        """Регистрация пользователя."""
        user_password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(user_password)
        user.save()

