import pandas as pd

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.wallets.models import Wallet
from rest_framework import status
from .models import Slip


class UploadSlipAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        if not file:
            return Response(
                {'error': 'Nenhum arquivo enviado'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            df = pd.read_excel(file)

            objects = list()
            for _, row in df.iterrows():
                wallet_name = request.POST.get('wallet')

                try:
                    wallet = Wallet.objects.get(name=wallet_name)
                except Wallet.DoesNotExist:
                    return Response(
                        {'error': f'Carteira "{wallet_name}" não encontrada.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                data_dict = row.to_dict()

                if 'Data Vencimento' in data_dict:
                    data_dict['due_date'] = data_dict.pop('Data Vencimento')

                if not wallet_name or not data_dict:
                    continue

                slip = Slip(wallet=wallet, json_result=data_dict)
                slip.save()

            return Response({'message': 'Boletos salvos com sucesso!'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
