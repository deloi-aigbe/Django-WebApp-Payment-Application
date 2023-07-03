from django.apps import AppConfig


# Define the configuration for the 'payment' app
class PaymentConfig(AppConfig):
    # Use a big integer primary key by default
    default_auto_field = "django.db.models.BigAutoField"
    # Set the name of the app to 'payment'
    name = "payment"
