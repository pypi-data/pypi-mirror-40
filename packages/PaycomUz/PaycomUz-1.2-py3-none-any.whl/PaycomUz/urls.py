from django.urls import path
from .views import MerchantAPIView



urlpatterns = [

   path('paycom',MerchantAPIView.as_view())

]