from django.db import models
from menu.models import Burger

class Pelanggan(models.Model):
    nama_pelanggan = models.CharField(max_length=255)
    pesanan = models.TextField()

    def __str__(self):
        return self.nama_pelanggan

class Pemesanan(models.Model):
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE)
    tanggal_pemesanan = models.DateTimeField(auto_now_add=True)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status_pembayaran = models.BooleanField(default=False)

    def __str__(self):
        return f"Pemesanan {self.id} oleh {self.pelanggan.nama}"

class DetailPemesanan(models.Model):
    pemesanan = models.ForeignKey(Pemesanan, on_delete=models.CASCADE)
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
