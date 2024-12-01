from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
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
