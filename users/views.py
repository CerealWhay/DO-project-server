from django.forms import model_to_dict
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from .logic.auth import Authenticator
from .logic.register import Registerer
from .serializers import RegisterSerializer, LoginSerializer, LoginResponseSerializer


class BaseAuthViewSet(ViewSet):
    """Вьюсет пользователей."""

    permission_classes = (permissions.AllowAny,)

    @action(methods=('post',), detail=False)
    def register(self, request):
        """Эндпоинт на регистрацию пользователя."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Registerer.register(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @action(methods=('post',), detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = Authenticator.login(
            serializer.validated_data.get('username'),
            serializer.validated_data.get('password'),
            request
        )
        serializer = LoginResponseSerializer(
            data=dict(token=token, user=model_to_dict(user))
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            data=serializer.validated_data, status=status.HTTP_200_OK
        )

    @action(methods=('post',), detail=False)
    def logout(self, request):
        """Логаут пользователя."""
        if not request.user.is_authenticated or request.auth is None:
            response = Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            Authenticator.logout(request.auth.key)
            response = Response(status=status.HTTP_200_OK)
        return response
