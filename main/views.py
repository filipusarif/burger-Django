from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pemesanan, Pelanggan, DetailPemesanan, Burger
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")  # Debug log
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'kasir':
                return redirect('kasir_dashboard')
            elif user.role == 'chef':
                return redirect('chef_dashboard')
            elif user.role == 'owner':
                return redirect('owner_dashboard')
        else:
            messages.error(request, "Username atau password salah.")
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# menu
def menu_list(request):
    burgers = Burger.objects.all()
    return render(request, 'menu_list.html', {'burgers': burgers})



# orders
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



# Reports
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
