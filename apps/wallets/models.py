from django.db import models

from apps.core.models import BaseModel


class Wallet(BaseModel):
    name = models.CharField(max_length=2048)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Carteira'
        verbose_name_plural = 'Carteiras'
        ordering = ['-created_at']
        db_table = 'wallets'
