from django.contrib import admin
from .models import Pelanggan, Pemesanan, DetailPemesanan

admin.site.register(Pelanggan)
admin.site.register(Pemesanan)
admin.site.register(DetailPemesanan)
