from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name="login-view"),
    path('chat/',views.chat_view,name="chat-view"),
    path('logout/',views.logout_view,name='logout-view'),
]
