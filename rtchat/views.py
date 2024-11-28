from django.shortcuts import render, redirect
from .models import GroupMessage
from django.contrib.auth import logout
from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
import os

def authenticate_user( request ):
    """
    A utility function to authenticate the user using JWT from the session.
    Returns:
        user (User): The authenticated user if successful.
        redirect_url (str): URL to redirect to if authentication fails.
    """
    access_token = request.session.get('access_token')

    if not access_token:
        return None, 'login'

    request_with_token = HttpRequest()
    request_with_token.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

    jwt_auth = JWTAuthentication()

    try:
        user, token = jwt_auth.authenticate(request_with_token)
        return user, None  # Return user if successful
    except AuthenticationFailed:
        return None, 'refresh'  # Invalid token, redirect to refresh

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    messages = GroupMessage.objects.all()
    return render(request,'rtchat/homepage.html',{'messages': messages})

def chat_view(request):
    user, redirect_url = authenticate_user(request)

    if user is not None:
        messages = GroupMessage.objects.all()
        return render(request,'rtchat/chat.html',{'messages': messages, 'user':user})
    else:
        return redirect(redirect_url)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Send request to /api/token/ endpoint
        token_url = os.getenv('TOKEN_URL', 'http://localhost:8000/api/token/')
        response = requests.post(token_url, data={'username':username, 'password':password})

        if response.status_code == 200:
            tokens = response.json()

            # Save the tokens in the session
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            return redirect('chat-view')
        
        else:
            return render(request,'rtchat/login.html',{'error': 'Invalid username or password'})

    return render(request,'rtchat/login.html')


def refresh(request):
    refresh_token = request.session['refresh_token']

    if not refresh_token:
        return redirect('login')

    # Send the refresh token to fetch access token
    refresh_url = os.getenv('REFRESH_URL', 'http://localhost:8000/api/token/refresh/')
    response = requests.post(refresh_url,data={'refresh':refresh_token})

    if response.status_code == 200:
        tokens = response.json()

        # Store the new access token
        request.session['access_token'] = tokens['access']
        return redirect('chat-view')
    
    else:
        return redirect('login')
