from common.models import mixins


class ReplacementStatus(mixins.BaseStatus):
    class Meta:
        verbose_name = 'Статус смены'
        verbose_name_plural = 'Статусы смены'


class BreakStatus(mixins.BaseStatus):
    class Meta:
        verbose_name = 'Статус обеда'
        verbose_name_plural = 'Статусы обедов'
