from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # menu
    path('menu/', views.menu_list, name='menu_list'),

    # orders
    path('create/', views.create_order, name='create_order'),
    path('receipt/<int:order_id>/', views.order_receipt, name='order_receipt'),

    # reports
    path('monthly/', views.monthly_report, name='monthly_report'),
]
