from django.contrib import admin
from .models import User, Burger, Pelanggan, Pemesanan, DetailPemesanan

admin.site.register(User)
admin.site.register(Burger)
admin.site.register(Pelanggan)
admin.site.register(Pemesanan)
admin.site.register(DetailPemesanan)
