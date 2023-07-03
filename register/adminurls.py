from django.urls import path
from .adminview import TransactionListView , CreateStaffUserView, UserListView 


app_name = "admin_privileges"

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_history"),
    #  path('create_staff_user/', register_admin_user, name='create_staff_user'),
    path('create_staff_user/', CreateStaffUserView.as_view(), name='create_staff_user'),
   path('user_list/', UserListView.as_view(), name='user_list'),
]