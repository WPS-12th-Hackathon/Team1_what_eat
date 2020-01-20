import requests
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

import hiddenkey
from .forms import LoginForm

# Create your views here.

User = get_user_model()
NAVER_ID = hiddenkey.naver_login_id
NAVER_SERECT = hiddenkey.naver_login_pw

def index(request):
    if request.user.is_authenticated:
        return redirect('restaurant:view_restaurant', page=1)
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

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': NAVER_ID,
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )

    context = {
        'login_url': login_url,
    }

    return render(request, 'members/signup.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return redirect('members:login')

    form = LoginForm()

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': NAVER_ID,
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )

    context = {
        'form': form,
        'login_url': login_url,
    }

    return render(request, 'members/login.html', context)


def log_out(request):
    logout(request)
    return redirect('index')


def shop_list(request):
    pass


def naver_login(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code or not state:
        return HttpResponse('code또는 state가 전달되지 않았습니다.')

    token_base_url = 'https://nid.naver.com/oauth2.0/token'
    token_params = {
        'grant_type': 'authorization_code',
        'client_id': NAVER_ID,
        'client_secret': NAVER_SERECT,
        'code': code,
        'state': state,
        'redirectURI': 'https://localhost:8000/members/naver-login/',
    }
    token_url = '{base}?{params}'.format(
        base=token_base_url,
        params='&'.join([f'{key}={value}' for key, value in token_params.items()])
    )
    response = requests.get(token_url)
    access_token = response.json()['access_token']

    me_url = 'https://openapi.naver.com/v1/nid/me'
    me_headers = {
        'Authorization': f'Bearer {access_token}',
    }
    me_response = requests.get(me_url, headers=me_headers)
    me_response_data = me_response.json()

    unique_id = me_response_data['response']['id']

    naver_username = f'n_{unique_id}'
    if not User.objects.filter(username=naver_username):
        user = User.objects.create_user(username=naver_username)
    else:
        user = User.objects.get(username=naver_username)

    login(request, user)
    return redirect('index')
