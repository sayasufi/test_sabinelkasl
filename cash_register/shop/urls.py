from django.urls import path
from .views import generate_receipt, get_all_items

urlpatterns = [
    path('cash_machine/', generate_receipt, name='generate_receipt'),
    path('items/', get_all_items, name='get_all_items'),
]