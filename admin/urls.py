from django.urls import path


from .views import admin_profile, login_admin, register_admin

urlpatterns = [
    path('register/', register_admin, name='register-admin'),
    path('login/', login_admin, name='login-admin'),
    path('profile/', admin_profile, name='admin-profile'),
]
