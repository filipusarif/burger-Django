from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pemesanan, Pelanggan, DetailPemesanan, Burger
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.functions import ExtractMonth
from calendar import month_name
from datetime import datetime
from .decorators import role_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Username: {username}, Password: {password}")  # Debug log
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'kasir':
                return redirect('burger')
            elif user.role == 'chef':
                return redirect('burger')
            elif user.role == 'owner':
                return redirect('dashboard')
        else:
            messages.error(request, "Username atau password salah.")
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# burger
@login_required
def burger_list(request):
    burgers = Burger.objects.all()
    return render(request, 'burger/read_burger.html', {'burgers': burgers})

@login_required
@role_required(['owner','kasir'])
def burger_add(request):
    if request.method == 'POST':
        nama = request.POST['nama']
        deskripsi = request.POST['deskripsi']
        harga = request.POST['harga']
        print('helo')
        Burger.objects.create(nama=nama, deskripsi=deskripsi, harga=harga)
        return redirect('burger')
    return render(request, 'burger/create_burger.html')

# Update burger
@login_required
@role_required(['owner','kasir'])
def burger_update(request, id):
    burger = get_object_or_404(Burger, id=id)
    if request.method == 'POST':
        burger.nama = request.POST['nama']
        burger.deskripsi = request.POST['deskripsi']
        burger.harga = request.POST['harga']
        burger.save()
        return redirect('burger')
    return render(request, 'burger/update_burger.html', {'burger': burger})

# Delete burger
@login_required
@role_required(['owner'])
def burger_delete(request, id):
    burger = get_object_or_404(Burger, id=id)
    if request.method == 'POST':
        burger.delete()
        return redirect('burger')
    return render(request, 'burger/delete_burger.html', {'burger': burger})



# Pelanggan
@login_required
@role_required(['owner','kasir'])
def pelanggan_list(request):
    pelanggans = Pelanggan.objects.all()
    return render(request, 'pelanggan/read_pelanggan.html', {'pelanggans': pelanggans})

@login_required
@role_required(['owner','kasir'])
def pelanggan_add(request):
    burgers = Burger.objects.all()  
    if request.method == 'POST':
        nama = request.POST.get('nama')  
        pelanggan = Pelanggan.objects.create(nama_pelanggan=nama)
        pelanggan.save() 
        return redirect('pelanggan')
    return render(request, 'pelanggan/create_pelanggan.html', {'burgers': burgers})



# Update pelanggan
@login_required
@role_required(['owner','kasir'])
def pelanggan_update(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)
    burgers = Burger.objects.all()  
   
    selected_burgers = pelanggan.pesanan.all().values_list('id', flat=True)
    if request.method == 'POST':
        nama = request.POST.get('nama') 
        pelanggan.nama_pelanggan = nama
        pelanggan.save()
        return redirect('pelanggan')
    return render(request, 'pelanggan/update_pelanggan.html', {
        'pelanggan': pelanggan,
        'burgers': burgers,
        'selected_burgers': selected_burgers
        })

# Delete pelanggan
@login_required
@role_required(['owner'])
def pelanggan_delete(request, id):
    pelanggan = get_object_or_404(Pelanggan, id=id)
    if request.method == 'POST':
        pelanggan.delete()
        return redirect('pelanggan')
    return render(request, 'pelanggan/delete_pelanggan.html', {'pelanggan': pelanggan})





# pemesanan
@login_required
@role_required(['owner','kasir'])
def pemesanan_list(request):
    pemesanans = Pemesanan.objects.all()
    return render(request, 'pemesanan/read_pemesanan.html', {'pemesanans': pemesanans})

@login_required
@role_required(['owner','kasir'])
def pemesanan_add(request):
    if request.method == 'POST':
        pelanggan_nama = request.POST.get('nama')
        burger_ids = request.POST.getlist('pesanan') 
        
        pelanggan = get_object_or_404(Pelanggan, nama_pelanggan=pelanggan_nama)
        burgers = Burger.objects.filter(id__in=burger_ids)  
        
        if not burgers:
            messages.error(request, "Anda harus memilih setidaknya satu burger.")
            return redirect('add_pemesanan')
        
        # Menghitung total harga dari semua burger
        total_harga = sum(burger.harga for burger in burgers)
        
        # Membuat objek pemesanan
        pemesanan = Pemesanan.objects.create(
            pelanggan=pelanggan,
            total_harga=total_harga,
            status_pembayaran=False
        )
        
        # Menambahkan burger ke pemesanan
        pemesanan.burger.set(burgers)  
        
        
        messages.success(request, "Pemesanan berhasil dibuat.")
        return redirect('pemesanan')  
    
    # Untuk request GET, render halaman dengan daftar pelanggan dan burger
    pelanggans = Pelanggan.objects.all()
    burgers = Burger.objects.all()
    return render(request, 'pemesanan/create_pemesanan.html', {'pelanggans': pelanggans, 'burgers': burgers})

# Update pemesanan
@login_required
@role_required(['owner','kasir'])
def pemesanan_update(request, id):
    pemesanan = get_object_or_404(Pemesanan, id=id)
    
    pelanggans = Pelanggan.objects.all()
    burgers = Burger.objects.all()

    selected_burgers = pemesanan.burger.all()

    if request.method == 'POST':
        pelanggan_nama = request.POST.get('nama')
        burger_ids = request.POST.getlist('pesanan')  
        
        pelanggan = get_object_or_404(Pelanggan, nama_pelanggan=pelanggan_nama)
        burgers = Burger.objects.filter(id__in=burger_ids)  
        
        if not burgers:
            messages.error(request, "Anda harus memilih setidaknya satu burger.")
            return redirect('update_pemesanan', id=id) 
        
        # Menghitung total harga dari semua burger
        total_harga = sum(burger.harga for burger in burgers)
        status_pembayaran = 'status_pembayaran' in request.POST
        # Mengupdate objek pemesanan
        pemesanan.pelanggan = pelanggan
        pemesanan.total_harga = total_harga
        pemesanan.status_pembayaran = status_pembayaran  
        pemesanan.save() 
        
        # Menambahkan atau memperbarui burger pada pemesanan
        pemesanan.burger.set(burgers) 
        burger=burgers[0]
        # Jika status_pembayaran True, menambahkan atau memperbarui DetailPemesanan
        if status_pembayaran:
            detail, created = DetailPemesanan.objects.get_or_create(
                pemesanan=pemesanan,
                burger=burger
            )
            pemesanan.burger.set(burgers)
        
        messages.success(request, "Pemesanan berhasil diperbarui.")
        return redirect('pemesanan')  

    return render(request, 'pemesanan/update_pemesanan.html', {
        'pemesanan': pemesanan,
        'pelanggans': pelanggans,
        'burgers': burgers,
        'selected_burgers': selected_burgers,
    })

# Delete pemesanan
@login_required
@role_required(['owner'])
def pemesanan_delete(request, id):
    pemesanan = get_object_or_404(Pemesanan, id=id)
    if request.method == 'POST':
        pemesanan.delete()
        return redirect('pemesanan')
    return render(request, 'pemesanan/delete_pemesanan.html', {'pemesanan': pemesanan})

# detail pemesanan
@login_required
def detail_list(request):
    details = DetailPemesanan.objects.all()
    return render(request, 'detail/read_detail.html', {'details': details})

@login_required
@role_required(['owner','kasir'])
def detail_add(request):
    burgers = Burger.objects.all()  
    if request.method == 'POST':
        nama = request.POST.get('nama')  
        detail = detail.objects.create(nama_detail=nama)
        detail.save() 
        return redirect('detail')
    return render(request, 'detail/create_detail.html', {'burgers': burgers})



# Update detail
@login_required
@role_required(['owner','kasir'])
def detail_update(request, id):
    detail = get_object_or_404(detail, id=id)
    burgers = Burger.objects.all()  
   
    selected_burgers = detail.pesanan.all().values_list('id', flat=True)
    if request.method == 'POST':
        nama = request.POST.get('nama') 
        detail.nama_detail = nama
        detail.save()
        return redirect('detail')
    return render(request, 'detail/update_detail.html', {
        'detail': detail,
        'burgers': burgers,
        'selected_burgers': selected_burgers
        })

# Delete detail
@login_required
@role_required(['owner'])
def detail_delete(request, id):
    detail = get_object_or_404(DetailPemesanan, id=id)
    if request.method == 'POST':
        detail.delete()
        return redirect('detail')
    return render(request, 'detail/delete_detail.html', {'detail': detail})

@login_required
@role_required(['owner','kasir'])
def detail_pemesanan_view(request, id):
    detail_pemesanan = DetailPemesanan.objects.get(id=id)
    return render(request, 'detail/detail_pemesanan.html', {
        'detail': detail_pemesanan
    })

# Reports
@login_required
@role_required(['owner'])
def dashboard(request):
    month = request.GET.get('month', None)
    transactions = Pemesanan.objects.all()
    if month:
        transactions = transactions.filter(tanggal_pemesanan__month=month)
    total_income = transactions.aggregate(Sum('total_harga'))['total_harga__sum'] or 0
    total_penjualan = DetailPemesanan.objects.aggregate(
        total=Sum('burger__harga')
    )['total'] or 0 


    penjualan_per_hari = (
        Pemesanan.objects.annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total_penjualan=Sum('total_harga'))
    )

    total_penjualan = sum(item['total_penjualan'] for item in penjualan_per_hari)
    jumlah_hari = len(penjualan_per_hari)
    rata_rata_penjualan = total_penjualan / jumlah_hari if jumlah_hari > 0 else 0


    total_pelanggan = Pelanggan.objects.count()
    selected_year = request.GET.get('tahun', datetime.now().year)
    print(selected_year)
    pemasukan_per_bulan = (
        Pemesanan.objects.filter(created_at__year=selected_year, status_pembayaran=True)  
        .annotate(month=ExtractMonth('created_at')) 
        .values('month')
        .annotate(total_pemasukan=Sum('total_harga'))
        .order_by('month')
    )

    # Data untuk chart
    labels = [month_name[item['month']] for item in pemasukan_per_bulan]
    print(labels)
    data = [float(item['total_pemasukan']) for item in pemasukan_per_bulan]

    burgers_data = (
        Pemesanan.objects.values('burger__nama') 
        .annotate(total=Count('id'))  
        .order_by('burger__nama')
    )

    burger_labels = [item['burger__nama'] for item in burgers_data]
    burger_counts = [item['total'] for item in burgers_data]

    # Data Pelanggan (jumlah pesanan berdasarkan pelanggan)
    pelanggan_data = (
        Pemesanan.objects.values('pelanggan__nama_pelanggan') 
        .annotate(total=Count('id')) 
        .order_by('-total')[:10]  
    )

    pelanggan_labels = [item['pelanggan__nama_pelanggan'] for item in pelanggan_data]
    pelanggan_counts = [item['total'] for item in pelanggan_data]

    

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'month': month,
        'total_penjualan':total_penjualan,
        'pemesanan_per_hari': rata_rata_penjualan,
        'total_pelanggan':total_pelanggan,
        'labels': labels,
        'data': data,
        'burger_labels': burger_labels,
        'burger_counts': burger_counts,
        'pelanggan_labels': pelanggan_labels,
        'pelanggan_counts': pelanggan_counts,
        'selected_year':selected_year,
    }

    return render(request, 'laporan/dashboard.html', context)


@login_required
@role_required(['owner'])
def view_laporan(request):
    burger_pemasukan = {}
    grand_total_pemasukan = 0
    tanggal_mulai = None
    tanggal_akhir = None
    status = False  

    if request.method == "POST":
        # Ambil tanggal mulai dan akhir dari form
        tanggal_mulai = request.POST.get('tanggal_mulai')
        tanggal_akhir = request.POST.get('tanggal_akhir')
        print("Filter tanggal mulai:", tanggal_mulai)
        print("Filter tanggal akhir:", tanggal_akhir)
        # print("Data Pemesanan:", pemesanan)
        print("Bis Pemasukan:", burger_pemasukan)

        if tanggal_mulai and tanggal_akhir:
            # Filter data Pemesanan berdasarkan rentang tanggal
            pemesanan = Pemesanan.objects.filter(
                created_at__date__gte=tanggal_mulai,
                created_at__date__lte=tanggal_akhir
            )

            if pemesanan.exists():  
                # Hitung total pemasukan per burger
                for burger in Burger.objects.all():
                    total_pemasukan = pemesanan.filter(burger=burger).aggregate(
                        total_pemasukan=Sum('total_harga')
                    )['total_pemasukan'] or 0
                    burger_pemasukan[burger.nama] = {
                        "total_pemasukan": total_pemasukan
                    }

                # Hitung total pemasukan semua pesanan
                grand_total_pemasukan = pemesanan.aggregate(
                    total=Sum('total_harga')
                )['total'] or 0

                status = True 
            else:
                status = False  

    context = {
        'burger_pemasukan': burger_pemasukan,
        'grand_total_pemasukan': grand_total_pemasukan,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
        'status': status,
    }
    return render(request, 'laporan/laporan.html', context)


@login_required
@role_required(['owner'])
def create_laporan(request):
    burger_pemasukan = {}
    grand_total_pemasukan = 0
    tanggal_mulai = None
    tanggal_akhir = None
    status=False

    if request.method == "POST":
        # Ambil tanggal mulai dan akhir dari form
        tanggal_mulai = request.POST.get('tanggal_mulai')
        tanggal_akhir = request.POST.get('tanggal_akhir')
        status = True

        if tanggal_mulai and tanggal_akhir:
            # Filter data Pemesanan berdasarkan rentang tanggal
            pemesanan = Pemesanan.objects.filter(
                created_at__date__gte=tanggal_mulai,
                created_at__date__lte=tanggal_akhir
            )

            # Hitung total pemasukan per burger
            for burger in Burger.objects.all():
                total_pemasukan = pemesanan.filter(burger=burger).aggregate(
                    total_pemasukan=Sum('total_harga')
                )['total_pemasukan'] or 0
                burger_pemasukan[burger.nama] = {
                    "total_pemasukan": total_pemasukan
                }

            # Hitung total pemasukan semua pesanan
            grand_total_pemasukan = pemesanan.aggregate(
                total=Sum('total_harga')
            )['total'] or 0

    context = {
        'burger_pemasukan': burger_pemasukan,
        'grand_total_pemasukan': grand_total_pemasukan,
        'tanggal_mulai': tanggal_mulai,
        'tanggal_akhir': tanggal_akhir,
        'status':status,
    }
    return render(request, 'laporan/create_laporan.html', context)