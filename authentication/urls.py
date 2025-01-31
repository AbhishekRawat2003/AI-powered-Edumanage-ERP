from django.urls import path
# authentication/urls.py
from .views import *
app_name = 'authentication'
urlpatterns = [
    path("", login_page, name='login_page'),
    # path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", doLogin, name='user_login'),
    path("logout/", logout_user, name='user_logout'),
]
