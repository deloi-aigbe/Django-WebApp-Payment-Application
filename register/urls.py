from django.urls import path

from .views import UserRegistrationView, LogoutView, UserLoginView, AccountSummaryView


app_name = "register"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", LogoutView.as_view(), name="user_logout"),
    path("register/", UserRegistrationView.as_view(), name="user_registration"),
    path("dashboard/", AccountSummaryView.as_view(), name="dashboard"),
]
