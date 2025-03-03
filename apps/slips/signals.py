from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import format_due_date
from .models import Slip
from ..sends.models import SlipMessage


@receiver(post_save, sender=Slip)
def create_slip_message(sender, instance, created, **kwargs):
    if created:
        due_date_str = instance.json_result.get('due_date')

        try:
            due_date = format_due_date(due_date_str)
        except ValueError as e:
            print(f'Erro ao formatar data: {e}')
            due_date = None

        if due_date:
            SlipMessage.objects.create(
                slip=instance,
                content=f'Novo boleto criado! Para = {instance.json_result.get('nome')}',
                date_vencit=due_date
            )
