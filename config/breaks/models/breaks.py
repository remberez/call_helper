from django.contrib.auth import get_user_model
from django.db import models
from .status import BreakStatus
from breaks.constants import *
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class Break(models.Model):
    replacement = models.ForeignKey(
        'breaks.Replacement', verbose_name='Перерыв',
        related_name='breaks', on_delete=models.CASCADE,
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Сотрудник', related_name='breaks',
    )
    break_start = models.TimeField(
        verbose_name='Начало обеда',
    )
    break_end = models.TimeField(
        verbose_name='Конец обеда',
    )
    status = models.ForeignKey(
        'breaks.BreakStatus', verbose_name='Статус обеда', null=False,
        blank=True, on_delete=models.RESTRICT,
    )

    class Meta:
        verbose_name = 'Обед'
        verbose_name_plural = 'Обеды'
        ordering = ('replacement__date', )

    def __str__(self):
        return f'Обед сотрудника {self.employee} №{self.pk}'

    def save(self, *args, **kwargs):
        try:
            status = self.status
        except ObjectDoesNotExist:
            if not self.pk:
                status, created = BreakStatus.objects.get_or_create(
                    code=BREAK_CREATED_STATUS,
                    defaults=BREAK_CREATED_STATUS_DEFAULT
                )
                self.status = status
        return super(Break, self).save(*args, **kwargs)

