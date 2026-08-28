from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('room/', views.virtual_classroom_view, name='virtual_classroom'),
]
