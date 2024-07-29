from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Replacement(models.Model):
    group = models.ForeignKey(
        'breaks.Group', related_name='group_replacements',
        verbose_name='Смена группы', on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        verbose_name='Дата смены',
    )
    break_start = models.TimeField(
        verbose_name='Начало обеда',
    )
    break_end = models.TimeField(
        verbose_name='Конец обеда',
    )
    break_max_duration = models.PositiveSmallIntegerField(
        verbose_name='Максимальная длительность обеда',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'
        ordering = ('-date',)

    def __str__(self):
        return f'Смена №{self.pk} группы {self.group}'


class ReplacementEmployee(models.Model):
    employee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Сотрудник смены', related_name='replacements',
    )
    replacement = models.ForeignKey(
        'breaks.Replacement', on_delete=models.SET_NULL,
        verbose_name='Смена', related_name='employees',
        null=True, blank=True,
    )
    status = models.ForeignKey(
        'breaks.ReplacementStatus', on_delete=models.RESTRICT,
        verbose_name='Статус смены', related_name='replacement_employees'
    )

    class Meta:
        verbose_name = 'Смена - работник'
        verbose_name_plural = 'Смены - работники'

    def __str__(self):
        return f'Смена {self.pk} для {self.employee}'
