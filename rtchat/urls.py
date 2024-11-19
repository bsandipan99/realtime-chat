from django.urls import path
from . import views

urlpatterns = [
    path('chat/',views.chat_view,name="chat-view"),
    path('logout/',views.logout_view,name='logout-view'),
    path('',views.login, name='login'),
    path('refresh/',views.refresh,name='refresh'),
]
