from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('GBP', 'British Pound'),
        ('NGN', 'Nigerian Naira'),
        ('EUR', 'Euro')
    ]

    base_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    target_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=5)
