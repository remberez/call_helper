from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self, email=None, phone_number=None, username=None, password=None, **extra_fields
    ):
        if not (email or username or phone_number):
            raise ParseError('Укажите email или номер телефона')

        if not username:
            if email:
                email = self.normalize_email(email)
                username = email.split('@')[0]
            else:
                username = phone_number

        user = self.model(**extra_fields)
        user.username = username
        if email:
            user.email = email

        if phone_number:
            user.phone_number = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email=None, username=None, phone_number=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, phone_number, username, password, **extra_fields)

    def create_user(
            self, email=None, username=None, phone_number=None, password=None, **extra_fields
    ):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, phone_number, username, password, **extra_fields)
