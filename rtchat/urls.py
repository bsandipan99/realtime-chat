from django.urls import path
from . import views

urlpatterns = [
    path('chat/',views.chat_view,name="chat-view"),
    path('logout/',views.logout_view,name='logout-view'),
    path('login/',views.login, name='login'),
    path('',views.home, name='home'),
    path('refresh/',views.refresh,name='refresh'),
]
