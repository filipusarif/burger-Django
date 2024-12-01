from django.shortcuts import render
from django.db.models import Sum
from orders.models import Pemesanan
from main.decorators import role_required


def monthly_report(request):
    month = request.GET.get('month', None)
    transactions = Pemesanan.objects.all()
    if month:
        transactions = transactions.filter(tanggal_pemesanan__month=month)
    total_income = transactions.aggregate(Sum('total_harga'))['total_harga__sum'] or 0
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'month': month,
    }
    return render(request, 'monthly_report.html', context)
