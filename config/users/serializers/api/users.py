import pdb

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from users.models.users import User
from users.serializers.nested.profle import ProfileSerializer


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

    def validate_email(self, value):
        # Проверка почты

        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError('Почта уже используется')
        return email

    def validate_password(self, value):
        # Проверка пароля

        validate_password(value)
        return value

    def create(self, validated_data):
        # Нужно переопределять, т.к. создание объекта на уровне DRF не
        # хэширует пароль. Получается так, что в базе хранится пароль
        # в открытом виде.
        User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )

    def validate(self, attrs):
        old = attrs['old_password']
        new = attrs['new_password']
        if old == new:
            raise ParseError('Пароли не должны совпадать.')
        return attrs

    def validate_old_password(self, value):
        instance = self.instance
        if not instance.check_password(value):
            raise ParseError('Неверный пароль.')
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data['new_password']
        instance.set_password(password)
        instance.save()
        return instance


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None
        instance = super().update(instance, validated_data)
        self._profile_update(instance.profile, profile_data)
        return instance

    def _profile_update(self, instance, validated_data):
        if validated_data:
            profile_serializer = ProfileSerializer(
                instance=instance, data=validated_data, partial=True
            )
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
