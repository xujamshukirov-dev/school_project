from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
    
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        rol = request.POST.get('rol')
        viloyat = request.POST.get('viloyat')
        tuman = request.POST.get('tuman')
        maktab_raqam = request.POST.get('maktab_raqam')
        sinf = request.POST.get('sinf')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon mavjud!")
        else:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                rol=rol,
                viloyat=viloyat,
                tuman=tuman,
                maktab_raqam=maktab_raqam,
                sinf=int(sinf) if sinf else None,
            )
            login(request, user)
            return redirect('dashboard')
    
    return render(request, 'accounts/register.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
