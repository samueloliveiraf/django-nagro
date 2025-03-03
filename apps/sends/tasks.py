from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from celery.utils.log import get_task_logger
from apps.sends.models import SlipMessage
from config.celery import app


logger = get_task_logger(__name__)



BRASIL_TZ = pytz.timezone('America/Sao_Paulo')


def is_commercial_hours():
    """
    Verifica se a hora atual está dentro do horário comercial no Brasil (9h - 18h).
    """
    now = datetime.now(BRASIL_TZ)
    if 9 <= now.hour < 18:
        return True
    return False


@app.task(name='task_sends_messages', queue='queue_sends_messages')
def task_sends_messages():
    """
    Função para enviar a mensagem, executando somente durante o horário comercial no Brasil.
    Envia as mensagens com data de vencimento entre 7 dias antes até a data atual.
    """
    if is_commercial_hours():
        today = timezone.now().date()
        target_date = today + timedelta(days=7)

        messages_to_send = SlipMessage.objects.filter(
            date_vencit__lte=target_date,
            send_due=False,
            is_active=True,
        )

        for message in messages_to_send:
            print(f"Enviando mensagem para o slip {message.slip.id}...")
            message.send_due = True
            message.save()
    else:
        print('Fora do horário comercial')
