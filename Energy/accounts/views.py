from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .backends import EmailBackend


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda automáticamente el usuario con contraseña encriptada
            login(request, user)
            return redirect('home')  # Reemplaza 'home' con la URL a la que deseas redirigir
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Utiliza el backend personalizado para autenticar
            user = authenticate(request, username=username, password=password, backend=EmailBackend)

            if user is not None:
                login(request, user)
                return redirect('home')  # Reemplaza 'home' con la URL a la que deseas redirigir
            else:
                messages.error(request, 'Credenciales incorrectas. Inténtalo nuevamente.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})
