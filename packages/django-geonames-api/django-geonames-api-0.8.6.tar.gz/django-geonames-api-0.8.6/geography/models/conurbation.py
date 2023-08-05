# Django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Conurbation(models.Model):

    country = models.ForeignKey(
        'geography.Country',
        on_delete=models.PROTECT,
        verbose_name=_('country')
    )
    region = models.ForeignKey(
        'geography.Region',
        on_delete=models.PROTECT,
        verbose_name=_('state')
    )
    department = models.ForeignKey(
        'geography.Department',
        on_delete=models.PROTECT,
        verbose_name=_('department')
    )
    name = models.CharField(_('Community name'), max_length=100)
    code = models.CharField(_('Community code'), max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("conurbation")
