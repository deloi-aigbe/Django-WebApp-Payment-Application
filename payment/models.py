# import necessary modules and models
from django.db import models
from register.models import User
from .constants import TRANSACTION_TYPE_CHOICES  # import constants from another file
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db.models.signals import (
    pre_save,
)  # signal to generate reference before saving to db
from django.dispatch import receiver


# create a Transaction model
class Transaction(models.Model):
    reference = models.CharField(
        max_length=32, unique=True
    )  # unique transaction reference
    sender = models.ForeignKey(  # sender of the transaction
        User, related_name="transactions_sent", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(  # receiver of the transaction
        User, related_name="transactions_received", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # amount requested
    sender_amount = models.DecimalField(
        decimal_places=2, max_digits=12
    )  # amount of the transaction
    receiver_amount = models.DecimalField(
        decimal_places=2, max_digits=12
    )  # amount of the transaction
    description = models.CharField(
        max_length=100, blank=True
    )  # optional description of the transaction
    transaction_type = models.CharField(
        max_length=6, default="DR"
    )  # type of the transaction (debit or credit)
    sender_email = models.CharField(max_length=100, blank=True)  # email of the sender
    receiver_email = models.CharField(
        max_length=100, blank=True
    )  # email of the receiver
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # timestamp of when the transaction was created
    currency = models.CharField(max_length=3)  # currency used in the transaction

    def __str__(self):
        return str(
            self.reference
        )  # return the reference of the transaction as a string

    class Meta:
        ordering = ["created_at"]  # order the transactions by creation time


# use signal to generate a reference for the transaction before saving to db
@receiver(pre_save, sender=Transaction)
def generate_reference(sender, instance, **kwargs):
    if not instance.reference:  # if reference does not exist
        instance.reference = get_random_string(length=10)  # generate a random reference


# create a MoneyRequest model
class MoneyRequest(models.Model):
    reference = models.CharField(
        max_length=32, unique=True
    )  # unique reference for the money request
    sender = models.ForeignKey(  # sender of the money request
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(  # receiver of the money request
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    sender_email = models.CharField(max_length=100, blank=True)  # email of the sender
    receiver_email = models.CharField(
        max_length=100, blank=True
    )  # email of the receiver
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # amount requested
    sender_amount = models.DecimalField(
        decimal_places=2, max_digits=12
    )  # amount of the transaction
    receiver_amount = models.DecimalField(
        decimal_places=2, max_digits=12
    )  # amount of the transaction
    description = models.CharField(
        max_length=100, blank=True
    )  # optional description of the request
    status = models.CharField(  # status of the money request
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # timestamp of when the money request was created

    def __str__(self):
        return str(
            self.reference
        )  # return the reference of the money request as a string

    class Meta:
        ordering = ["created_at"]  # order the money requests by creation time


# use signal to generate a reference for the money request before saving to db
@receiver(pre_save, sender=MoneyRequest)
def generate_reference(sender, instance, **kwargs):
    if not instance.reference:  # if reference does not exist
        instance.reference = get_random_string(length=10)
