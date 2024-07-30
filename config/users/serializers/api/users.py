from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from users.models.users import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Что бы пароль не возвращался в ответе
    email = serializers.EmailField()  # Без этой строки не работает проверка email

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password'
        )

    # Проверка почты
    def validate_email(self, value):
        print(52)
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('Почта уже используется')
        return email

    # Проверка пароля
    def validate_password(self, value):
        validate_password(value)
        return value
