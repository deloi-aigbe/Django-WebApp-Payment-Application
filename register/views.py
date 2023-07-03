from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from payment.models import Transaction
from django.db.models import Sum

from django.http import HttpResponseForbidden
    

from .forms import UserRegistrationForm


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/user_registration.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy("payments:payment_history"))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)

        if registration_form.is_valid():
            user = registration_form.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f"Thank You For Creating A Bank Account. "
                    f"Your Account Number is {user.account_no}. "
                ),
            )
            return HttpResponseRedirect(reverse_lazy("payments:payment_history"))

        return self.render_to_response(
            self.get_context_data(registration_form=registration_form)
        )

    def get_context_data(self, **kwargs):
        if "registration_form" not in kwargs:
            kwargs["registration_form"] = UserRegistrationForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name = "accounts/user_login.html"
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect(reverse_lazy("accounts:dashboard"))
        return super().dispatch(request, *args, **kwargs)


class AccountSummaryView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        total_sent = (
            Transaction.objects.filter(sender=user).aggregate(total_sent=Sum("sender_amount"))[
                "total_sent"
            ]
            or 0
        )
        total_received = (
            Transaction.objects.filter(receiver=user).aggregate(
                total_received=Sum("receiver_amount")
            )["total_received"]
            or 0
        )
        balance = user.balance
        total_requests_sent = user.sent_requests.count()
        total_requests_received = user.received_requests.count()
        balance = user.balance
        context = {
            "total_sent": f"{user.default_currency} {total_sent}",
            "total_received": f"{user.default_currency} {total_received}",
            "total_requests_sent": total_requests_sent,
            "total_requests_received": total_requests_received,
            "balance": f"{user.default_currency} {balance}",
        }
        return render(request, "index.html", context)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("admin_privileges:transaction_history")
        return super().dispatch(request, *args, **kwargs)





class LogoutView(RedirectView):
    pattern_name = "home"

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)
