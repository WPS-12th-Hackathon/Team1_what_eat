from django.contrib.auth import get_user_model, login, authenticate, logout
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm

# Create your views here.


User = get_user_model()


def index(request):
    return render(request, 'index.html')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return HttpResponse('이미 사용중인 username 입니다.')
        if User.objects.filter(email=email).exists():
            return HttpResponse('이미 사용중인 email 입니다.')

        user = User.objects.create_user(
            password=password,
            username=username,
            email=email,
            name=name,
            )

        login(request, user)
        return redirect('index')
    return render(request, 'members/signup.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('members:login')

    form = LoginForm()
    context = {
        'form': form,
    }

    return render(request, 'members/login.html', context)


def log_out(request):
    logout(request)
    return redirect('index')

