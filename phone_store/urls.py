from django.urls import path
from .views import home, checkout

urlpatterns = [
    path('', home, name='home'),
    path('/checkout', checkout, name='checkout'),
]
