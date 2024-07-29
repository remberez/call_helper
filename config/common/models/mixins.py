from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseStatus(models.Model):
    code = models.CharField(
        max_length=16, primary_key=True, verbose_name='Код статуса',
    )
    name = models.CharField(
        max_length=32, verbose_name='Название статуса',
    )
    sort = models.PositiveSmallIntegerField(
        verbose_name='Сортировка', null=True, blank=True,
    )
    is_active = models.BooleanField(
        default=True, verbose_name='Активность статуса',
    )

    class Meta:
        ordering = ('sort', )
        abstract = True

    def __str__(self):
        return f'{self.code}, {self.name}'
