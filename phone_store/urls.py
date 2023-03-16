from django.urls import path
from .views import (home, cart, updateItem, deleteItem, checkout)

urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('update_item/', updateItem, name='update_item'),
    path('delete_item/', deleteItem, name='delete_item'),
    path('checkout/', checkout, name='checkout')
]
