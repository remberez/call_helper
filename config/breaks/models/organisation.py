from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Organisation(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Название'
    )
    director = models.ForeignKey(
        User, related_name='organisations',
        on_delete=models.RESTRICT, verbose_name='Директор'
    )
    employees = models.ManyToManyField(
        User, related_name='employee_organisation',
        blank=True, verbose_name='Сотрудники',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'{self.name}'
