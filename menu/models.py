from django.db import models

class Burger(models.Model):
    nama = models.CharField(max_length=255)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nama
