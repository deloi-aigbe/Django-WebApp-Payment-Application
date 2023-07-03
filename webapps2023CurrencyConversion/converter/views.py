# Create your views here.
from rest_framework.views import APIView
from django.shortcuts import render
from .serializers import ExchangeRateSerializer
from .models import ExchangeRate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView

class GetRateView(APIView):
    def get(self, request):
        base_currency = request.query_params.get('base_currency')
        target_currency = request.query_params.get('target_currency')

        try:
            exchange_rate = ExchangeRate.objects.get(
                base_currency=base_currency,
                target_currency=target_currency
            )
            serializer = ExchangeRateSerializer(exchange_rate)
            return Response(serializer.data)
        except ExchangeRate.DoesNotExist:
            return Response({'error': 'Exchange rate not found'})

class ConvertView(APIView):
    def get(self, request):
        base_currency = request.query_params.get('base_currency')
        target_currency = request.query_params.get('target_currency')
        amount = request.query_params.get('amount')

        print(base_currency, target_currency, amount)
        try:
            exchange_rate = ExchangeRate.objects.get(
                base_currency=base_currency,
                target_currency=target_currency
            )
            converted_amount = float(amount) * float(exchange_rate.exchange_rate)
            return Response({'converted_amount': converted_amount})
        except ExchangeRate.DoesNotExist:
            return Response({'error': 'Exchange rate not found'})
