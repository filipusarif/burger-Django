from django.shortcuts import render, get_object_or_404
from .models import Pemesanan, Pelanggan, DetailPemesanan
from main.decorators import role_required


def create_order(request):
    if request.method == 'POST':
        # Logika untuk membuat pesanan baru
        pass
    return render(request, 'orders/create_order.html')



def order_receipt(request, order_id):
    order = get_object_or_404(Pemesanan, id=order_id)
    details = order.detailpemesanan_set.all()
    context = {
        'order': order,
        'details': details
    }
    return render(request, 'receipt.html', context)
