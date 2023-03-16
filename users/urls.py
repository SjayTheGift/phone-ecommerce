from django.urls import path
from .views import RegisterView, ProfileView, change_password, MyLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='account_register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('mylogin/', MyLoginView.as_view(), name='login' ),
    path('change_password/', change_password, name='change_password'),
]