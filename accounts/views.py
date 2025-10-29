from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.POST.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('list_activities') 
        else:
            error_message = 'Nome de usuário ou senha inválidos.'
    context = {
        'error': error_message,
    }
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')
