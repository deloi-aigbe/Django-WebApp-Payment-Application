# Import necessary functions and views from the views module
from django.urls import path
from .views import (
    TransactionCreateView,
    TransactionListView,
    MoneyRequestCreateView,
    MoneyRequestReceivedListView,
    MoneyRequestSentListView,
)

# Set the app name to "register"
app_name = "register"

# Define the URL patterns for the register app
urlpatterns = [
    # Map the "money-request/" URL to the MoneyRequestCreateView class and name it "money_request"
    path("money-request/", MoneyRequestCreateView.as_view(), name="money_request"),
    # Map the "request-sent/" URL to the MoneyRequestSentListView class and name it "request_sent"
    path("request-sent/", MoneyRequestSentListView.as_view(), name="request_sent"),
    # Map the "request-received/" URL to the MoneyRequestReceivedListView class and name it "request_received"
    path(
        "request-received/",
        MoneyRequestReceivedListView.as_view(),
        name="request_received",
    ),
    # Map the "transactions/" URL to the TransactionListView class and name it "payment_history"
    path("transactions/", TransactionListView.as_view(), name="payment_history"),
    # Map the "send-money/" URL to the TransactionCreateView class and name it "make_payment"
    path("send-money/", TransactionCreateView.as_view(), name="make_payment"),
]
