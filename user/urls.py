from django.urls import path
from . views import register_user, user_login, user_logout, home_view, verify


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', user_login, name='login'),
    path('registration/', register_user, name='register'),
    path('logout/', user_logout, name='logout'),
    path('verify/', verify, name='verify'),
]