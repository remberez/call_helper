from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from users.models.managers import CustomUserManager
from users.models.profile import Profile


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм', unique=True,
        null=True, blank=True, max_length=25,
    )
    email = models.EmailField(
        verbose_name='Почта', unique=True, null=True, blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name='Телефон', unique=True, null=True, blank=True
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.phone_number}"


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(
            user=instance,
        )
