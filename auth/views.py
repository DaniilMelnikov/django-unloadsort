from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/start/?page=1')
    else:
        form = RegisterForm()
        return render(request, 'auth/registration.html', {'form': form})
    

def success_register(request):
    form= RegisterForm(request.POST or None)
    if form.is_valid():
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = User.objects.create_user(
            username=email,
            email=email, 
            password=password, 
            first_name=first_name, 
            last_name=last_name
            )
        
        user.save()

        return redirect('/login/')
    else:
        form = RegisterForm()
        return render(request, 'auth/registration.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/start/?page=1')
    else:
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form, 'error': ''})
    

def success_login(request):
    form= LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request=request, username=email, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/start/?page=1')  
        else:
            return render (request, 'auth/login.html', {'form': form, 'error': 'Неверный Email или Парольы'})
        

def logout_view(request):
    logout(request)
    form = LoginForm()
    return render (request, 'auth/login.html', {'form': form, 'error': ''})