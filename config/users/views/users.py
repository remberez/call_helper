import pdb

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from users.serializers.api.users import UserSerializer, ChangePasswordSerializer, MeSerializer

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=['Аутентификация & Авторизация'],
    )
)
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


@extend_schema_view(
    patch=extend_schema(
        summary='Смена пароля',
        tags=['Аутентификация & Авторизация'],
        request=ChangePasswordSerializer,
    )
)
class ChangePasswordView(APIView):
    def patch(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(
            instance=user, data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        summary='Информация о пользователе',
        tags=['Пользователи'],
    ),
    patch=extend_schema(
        summary='Изменить данные',
        tags=['Пользователи'],
    ),
)
class MeView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = MeSerializer
    http_method_names = ('patch', 'get')

    def get_object(self):
        return self.request.user
