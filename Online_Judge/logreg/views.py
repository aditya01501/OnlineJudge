from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Get the custom user model
User = get_user_model()

def register(request):
    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        email =  request.POST.get("email") 
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'User with this username already exists')
            return redirect("/LogIn/register")
        user = User.objects.create_user(username=username, phone_number = phone_number, email = email)
        user.set_password(password)
        user.save()
    context = {} 
    return render(request, 'Register.html', context)

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'User with this username does not exist')
            return redirect('/LogIn/login/')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, 'Invalid password')
            return redirect('/LogIn/login')

        login(request, user)
        messages.info(request, 'Login successful')
        return redirect('/User/HomePage/')
    
    context = {}
    return render(request, 'login.html', context)


def Logout(request):
    logout(request)
    return redirect('/login/login')