from django.db import models

from apps.core.models import BaseModel
from apps.wallets.models import Wallet


class Slip(BaseModel):
    json_result = models.JSONField()
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT, related_name='slips')

    class Meta:
        verbose_name = 'Boleto'
        verbose_name_plural = 'Boletos'
        ordering = ['-created_at']
        db_table = 'slips'
