from django.urls import path
from .views import GetRateView, ConvertView

app_name = "conversion"

urlpatterns = [
    path('getRate/', GetRateView.as_view()),
    path('convert/', ConvertView.as_view()),
]
