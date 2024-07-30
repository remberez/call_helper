from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from common.models.managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм', unique=True,
        null=True, blank=True, max_length=25,
    )
    email = models.CharField(
        verbose_name='Почта', unique=True, null=True, blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон', unique=True, null=True,
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.phone_number}"
