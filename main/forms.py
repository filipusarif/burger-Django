from django import forms
from .models import Pemesanan, DetailPemesanan

class OrderForm(forms.ModelForm):
    class Meta:
        model = Pemesanan
        fields = ['pelanggan', 'status_pembayaran']

class DetailOrderForm(forms.ModelForm):
    class Meta:
        model = DetailPemesanan
        fields = ['burger', 'jumlah']