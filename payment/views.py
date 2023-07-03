from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, FormView
from django.views import View
from .constants import TRANSACTION_TYPE_CHOICES
from .forms import TransactionForm, MoneyRequestForm, MoneyRequestUpdateForm
from .models import Transaction, MoneyRequest
from register.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q, F
from .conversion_helper import convert


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "payments/payment.html"
    success_url = reverse_lazy("payments:payment_history")

    def form_valid(self, form):
        sender = self.request.user
        sender_email = sender.email
        form.sender = sender
        transaction = form.save(commit=False)
        transaction.sender = sender
        if sender.balance < transaction.amount:
            form.add_error("amount", "Insufficient balance")
            return super().form_invalid(form)
        transaction.receiver = form.cleaned_data["receiver"]
        receiver_amount = convert(
            sender.default_currency, transaction.receiver.default_currency, transaction.amount
        )
        transaction.sender_email = sender_email
        transaction.sender_amount = transaction.amount
        transaction.receiver_amount = receiver_amount
        transaction.save()

        sender.balance = F("balance") - transaction.sender_amount
        sender.save()

        # Update receiver balance
        transaction.receiver.balance = F("balance") + receiver_amount
        transaction.receiver.save()

        return super().form_valid(form)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "payments/payment_history.html"
    paginate_by = 10  # Number of transactions per page


    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(Q(sender=user) | Q(receiver=user)).order_by(
            "-created_at"
        )

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)


class MoneyRequestCreateView(LoginRequiredMixin, CreateView):
    model = MoneyRequest
    form_class = MoneyRequestForm
    template_name = "payments/money_request.html"
    success_url = reverse_lazy("payments:request_sent")

    def form_valid(self, form):
        sender_email = self.request.user.email
        sender = User.objects.get(email=sender_email)
        money_requests = form.save(commit=False)
        money_requests.receiver = form.cleaned_data["receiver"]
        money_requests.sender = sender
        receiver_amount = convert(sender.default_currency, money_requests.receiver.default_currency, money_requests.amount)
        money_requests.receiver_amount = receiver_amount
        money_requests.sender_amount = money_requests.amount
        money_requests.save()
        return super().form_valid(form)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)


class MoneyRequestSentListView(LoginRequiredMixin, ListView):
    model = MoneyRequest
    template_name = "payments/money_requests_sent.html"
    paginate_by = 10  # Number of transactions per page


    def get_queryset(self):
        return MoneyRequest.objects.filter(sender=self.request.user).order_by(
            "-created_at"
        )


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)

class MoneyRequestReceivedListView(LoginRequiredMixin, ListView):
    model = MoneyRequest
    template_name = "payments/money_requests_received.html"
    success_url = reverse_lazy("payments:payment_history")
    paginate_by = 10  # Number of transactions per page


    def get_queryset(self):
        return MoneyRequest.objects.filter(receiver=self.request.user).order_by(
            "-created_at"
        )

    def post(self, request, *args, **kwargs):
        money_request = MoneyRequest.objects.get(
            id=request.POST["accept"]
            if "accept" in request.POST
            else request.POST["reject"]
        )

        if "accept" in request.POST:
            if money_request.status != "pending":
                return redirect("payments:payment_history")
            if money_request.receiver_email == money_request.sender_email:
                messages.error(request, "You cannot send money to yourself")
                return redirect("payments:request_received")
            if money_request.sender.balance < money_request.receiver_amount:
                messages.error(request, "Insufficient balance")
                return redirect("payments:request_received")
            send_money(
                money_request.sender,
                money_request.receiver,
                money_request.receiver_email,
                money_request.sender_email,
                money_request.sender_amount,
                money_request.receiver_amount
            )
            money_request.status = "accepted"
            money_request.save()
            messages.success(request, "Money request accepted")
            return redirect("payments:payment_history")
        elif "reject" in request.POST:
            if money_request.status != "pending":
                return redirect("payments:request_received")
            money_request.status = "rejected"
            money_request.save()
            messages.success(request, "Money request rejected")
            return redirect("payments:request_received")


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)


def send_money(sender, receiver, receiver_email, sender_email, sender_amount, receiver_amount):
    receiver.balance = F("balance") - receiver_amount
    receiver.save()
    sender.balance = F("balance") + sender_amount
    sender.save()

    transaction = Transaction(
        receiver=sender,
        sender=receiver,
        sender_amount=receiver_amount,
        receiver_amount=sender_amount,
        receiver_email=sender_email,
        sender_email=receiver_email,
        description="money request accepted",
    )
    transaction.save()



    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)
