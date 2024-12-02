from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # burger
    path('burger/', views.burger_list, name='burger'),
    path('burger/add', views.burger_add, name='add_burger'),
    path('burger/update/<int:id>/', views.burger_update, name='update_burger'),
    path('burger/delete/<int:id>/', views.burger_delete, name='delete_burger'),

    # pelanggan
    path('pelanggan/', views.pelanggan_list, name='pelanggan'),
    path('pelanggan/add/', views.pelanggan_add, name='add_pelanggan'),
    path('pelanggan/update/<int:id>/', views.pelanggan_update, name='update_pelanggan'),
    path('pelanggan/delete/<int:id>/', views.pelanggan_delete, name='delete_pelanggan'),

    # pemesanan
    path('pemesanan/', views.pemesanan_list, name='pemesanan'),
    path('pemesanan/add/', views.pemesanan_add, name='add_pemesanan'),
    path('pemesanan/update/<int:id>/', views.pemesanan_update, name='update_pemesanan'),
    path('pemesanan/delete/<int:id>/', views.pemesanan_delete, name='delete_pemesanan'),

    # detail pemesanan
    path('detail/', views.detail_list, name='detail'),
    path('detail/add/', views.detail_add, name='add_detail'),
    path('detail/update/<int:id>/', views.detail_update, name='update_detail'),
    path('detail/delete/<int:id>/', views.detail_delete, name='delete_detail'),

    # orders
    path('nota/<int:id>/', views.detail_pemesanan_view, name='detail_pemesanan_view'),

    # reports
    path('view/', views.view_laporan, name='view_laporan'),
    path('laporan/', views.create_laporan, name='laporan'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
