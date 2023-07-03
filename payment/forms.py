import datetime
from django import forms
from django.conf import settings
from .models import Transaction
from register.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import MoneyRequest


class TransactionForm(forms.ModelForm):
    receiver_email = forms.EmailField()

    class Meta:
        model = Transaction
        fields = ("receiver_email", "amount", "description", "sender_email")

    def clean(self):
        # Call the superclass clean() method to get cleaned form data
        cleaned_data = super().clean()
        receiver_email = cleaned_data.get("receiver_email")
        sender_email = cleaned_data.get("sender_email")

        try:
            # Try to get the User objects for the sender and receiver
            receiver = User.objects.get(email=receiver_email)
            sender = User.objects.get(email=sender_email)

        except User.DoesNotExist:
            raise ValidationError("The receiver email address is invalid.")

        # Check if the sender is trying to send money to themselves
        if receiver == sender:
            raise forms.ValidationError("You cannot send money to yourself")

        # Add the receiver object to the cleaned data
        cleaned_data["receiver"] = receiver
        return cleaned_data


class MoneyRequestForm(forms.ModelForm):
    receiver_email = forms.EmailField()

    class Meta:
        model = MoneyRequest
        fields = ("receiver_email", "amount", "description", "sender_email")

    def clean(self):
        cleaned_data = super().clean()
        receiver_email = cleaned_data.get("receiver_email")
        sender_email = cleaned_data.get("sender_email")

        try:
            receiver = User.objects.get(email=receiver_email)
            sender = User.objects.get(email=sender_email)

        except User.DoesNotExist:
            raise ValidationError("The receiver email address is invalid.")

        if receiver == sender:
            raise forms.ValidationError("You cannot request money from yourself")

        cleaned_data["receiver"] = receiver
        return cleaned_data


class MoneyRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = MoneyRequest
        fields = ("status",)
