from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    organisation = models.ForeignKey(
        'breaks.Organisation', related_name='organisation_groups',
        verbose_name='Организация', on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=255, verbose_name='Название группы',
    )
    manager = models.ForeignKey(
        User, related_name='manager_groups',
        verbose_name='Менеджер группы', on_delete=models.SET_NULL,
        null=True, blank=True,
    )
    employees = models.ManyToManyField(
        User, related_name='employee_group',
        blank=True, verbose_name='Сотрудники',
    )
    min_active = models.PositiveSmallIntegerField(
        verbose_name='Минимальное количество активных сотрудников',
        null=True, blank=True,
    )
    break_start = models.TimeField(
        verbose_name='Начало обеда',
    )
    break_end = models.TimeField(
        verbose_name='Конец обеда',
    )
    break_max_duration = models.PositiveSmallIntegerField(
        verbose_name='Максимальная длительность обеда'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('organisation__name', )

    def __str__(self):
        return f'{self.name}'
