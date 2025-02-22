from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.conf import settings
import os

# Inscription
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)

            user_directory = os.path.join(settings.MEDIA_ROOT, 'uploads', f'user_{user.id}')
            
            if not os.path.exists(user_directory):
                os.makedirs(user_directory)
                
            return redirect('desktop')  # Redirige vers le bureau après inscription
        

        
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Connexion
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('desktop')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')
