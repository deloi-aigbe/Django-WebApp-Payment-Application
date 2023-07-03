from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from payment.conversion_helper import convert

base_currency = "USD"
base_amount = 1000

from .models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control  ", "autofocus": "on" })
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": "form-control  ", "autofocus": "off"})
    )
    default_currency = forms.ChoiceField(
        choices=[("GBP", "GBP"), ("EUR", "EUR"), ("NGN", "NGN"), ("USD", "USD")],
        widget=forms.Select(attrs={"class": "form-control", "autofocus": "off"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "default_currency",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    "class": (
                        "appearance-none block w-full bg-gray-200 "
                        "text-gray-700 border border-gray-200 "
                        "rounded py-3 px-4 leading-tight "
                        "focus:outline-none focus:bg-white "
                        "focus:border-gray-500"
                    )
                }
            )

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.default_currency = self.cleaned_data.get("default_currency")
            user.balance = convert(base_currency, user.default_currency, base_amount)
            user.save()
            user.account_no = user.id + settings.ACCOUNT_NUMBER_START_FROM
            user.save()
        return user
