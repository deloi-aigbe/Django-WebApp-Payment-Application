from django.contrib import admin
from .models import Transaction, MoneyRequest


# Define a custom admin interface for the Transaction model
# class TransactionAdmin(admin.ModelAdmin):
#     # Display these fields as columns in the admin interface list view
#     list_display = ("reference", "sender", "receiver", "amount", "description")
#     # These fields cannot be edited in the admin interface
#     readonly_fields = ("reference", "created_at")

#     # Override the default save method to update sender and receiver balances and transaction type
#     def save_model(self, request, obj, form, change):
#         # Determine the type of the transaction (debit or credit) based on the current user
#         if obj.sender == request.user:
#             obj.transaction_type = "debit"
#         elif obj.receiver == request.user:
#             obj.transaction_type = "credit"

#         # If this is a debit transaction and the sender has insufficient funds, raise an error
#         if obj.transaction_type == "debit" and obj.sender.balance < obj.amount:
#             raise ValueError(
#                 "Sender does not have enough balance to make this transaction."
#             )

#         # Update the sender and receiver balances based on the transaction amount and type
#         if obj.transaction_type == "credit":
#             obj.receiver.balance += obj.amount
#             obj.receiver.save()
#             obj.sender.balance -= obj.amount
#             obj.sender.save()
#         elif obj.transaction_type == "debit":
#             obj.sender.balance += obj.amount
#             obj.sender.save()
#             obj.receiver.balance -= obj.amount
#             obj.receiver.save()

#         # Save the transaction instance
#         obj.save()


# Register the Transaction and MoneyRequest models with the admin site, using the custom TransactionAdmin interface
admin.site.register(Transaction)
admin.site.register(MoneyRequest)
