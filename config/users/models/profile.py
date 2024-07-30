from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        'users.User', verbose_name='Пользователь',
        on_delete=models.CASCADE, related_name='profile',
    )
    telegram_id = models.CharField(
        verbose_name='Телеграм ID', max_length=25, null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.id} {self.user.username} профиль'
