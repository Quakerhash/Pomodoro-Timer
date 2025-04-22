from django.urls import path
from . import views
urlpatterns = [
   path('', views.login_register, name='login'),
    path('otp/',views.otp,name='otp'),
    path('resendotp/',views.resend_otp,name='rotp'),
]