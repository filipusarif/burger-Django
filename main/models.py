from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('kasir', 'Kasir'),
        ('chef', 'Chef'),
        ('owner', 'Owner'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

# Menu
class Burger(models.Model):
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nama


# orders
class Pelanggan(models.Model):
    nama_pelanggan = models.CharField(max_length=255)
    pesanan = models.ManyToManyField('Burger', related_name='pelanggans')

    def __str__(self):
        return self.nama_pelanggan

class Pemesanan(models.Model):
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE)
    burger = models.ManyToManyField(Burger)
    total_harga = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status_pembayaran = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Pemesanan {self.id} oleh {self.pelanggan.nama}"

class DetailPemesanan(models.Model):
    pemesanan = models.ForeignKey(Pemesanan, on_delete=models.CASCADE)
    burger = models.ForeignKey(Burger, on_delete=models.CASCADE)
