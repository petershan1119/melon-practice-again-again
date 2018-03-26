import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect

User = get_user_model()

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    login(request, user)
    return redirect('index')


def facebook_login_backup(request):
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_SECRET_CODE
    code = request.GET['code']
    redirect_uri = 'http:/localhost:8000/facebook-login/'

    url = 'https://graph.facebook.com/v2.12/oauth/access_token'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.get(url, params)
    response_dict = response.json()
    for key, value in response_dict.items():
        print(f'{key}: {value}')

    url = 'https://graph.facebook.com/v2.12/me'
    params = {
        'access_token': response_dict['access_token'],
        'fields': ','.join([
            'id',
            'name',
            'picture.width(2500)',
            'first_name',
            'last_name',
        ])
    }
    response = requests.get(url, params)
    response_dict = response.json()
    facebook_id = response_dict['id']
    name = response_dict['name']
    first_name = response_dict['first_name']
    last_name = response_dict['last_name']
    url_picture = response_dict['picture']['data']['url']

    if User.objects.filter(username=facebook_id):
        user = User.objects.get(username=facebook_id)
    else:
        user = User.objects.create_user(
            username=facebook_id,
            first_name=first_name,
            last_name=last_name,
        )
    login(request, user)
    return redirect('index')
