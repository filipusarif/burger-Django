from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('receipt/<int:order_id>/', views.order_receipt, name='order_receipt'),
]