from django.db import models

from apps.core.models import BaseModel
from apps.slips.models import Slip


class DelinquentDueChoices(models.TextChoices):
    YES = 'YE'
    NO = 'NO'


class SlipMessage(BaseModel):
    slip = models.ForeignKey(Slip, on_delete=models.CASCADE, related_name='messages')
    delinquent_due = models.CharField(
        max_length=2,
        choices=DelinquentDueChoices,
        default=DelinquentDueChoices.NO
    )
    send_due = models.BooleanField(default=False)
    content = models.TextField()
    date_vencit = models.DateField(null=False, blank=False)

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['-created_at']
        db_table = 'slip_messages'
