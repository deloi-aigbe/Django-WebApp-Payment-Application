
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView , CreateView
from payment.models import Transaction
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.db.models import Q
from register.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required





class TransactionListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Transaction
    template_name = "Admin/all_transaction_history.html"
    paginate_by = 10  # Number of transactions per page

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.all().order_by("-created_at")

    def test_func(self):
        return self.request.user.is_staff







# @login_required
class CreateStaffUserView(LoginRequiredMixin,UserPassesTestMixin,  CreateView):
    model = User
    fields = ['username', 'password', 'email', 'is_staff']
    template_name = 'Admin/staff_user_create.html'
    success_url = reverse_lazy('admin_privileges:transaction_history')

    def form_valid(self, form):
        user = form.save(commit=False)

        print(form)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff





class UserListView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    model = User
    template_name = 'Admin/all_user_list.html'
    paginate_by = 10
    context_object_name = 'users'


    def test_func(self):
        return self.request.user.is_staff