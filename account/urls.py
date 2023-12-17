from django.urls import path, include
from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('account_activation_sent/', AccountActivationSent.as_view(), name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', Activate.as_view(), name='activate'),
    path('account_activation_complete/', AccountActivationComplete.as_view(), name='account_activation_complete'),
]