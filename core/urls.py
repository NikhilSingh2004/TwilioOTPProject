from django.urls import path
from core import views

urlpatterns = [
    path('', views.Home.as_view(), name="Home"),
    path('signup/', views.SignUp.as_view(), name="SignUp"),
    path('login/', views.LogIn.as_view(), name="LogIn"),
    path('profile/', views.UserHome.as_view(), name="UserHome"),
    # path('otp/', views.OTP.as_view(), name="OTP"),
    path('otp/<uid>/', views.OTP.as_view(), name="OTP"),
]
