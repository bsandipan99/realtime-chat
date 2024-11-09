from django.shortcuts import render, redirect
from .models import GroupMessage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('chat-view')
        else:
            return render(request, 'rtchat/login.html', {'error': 'Invalid username or password'})
    
    return render(request,'rtchat/login.html',)

def logout_view(request):
    logout(request)
    return redirect('login-view')

@login_required
def chat_view(request):
    messages = GroupMessage.objects.all()
    return render(request,'rtchat/chat.html',{'messages': messages})
