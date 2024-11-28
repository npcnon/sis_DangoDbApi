#users.urls

from django.urls import path
from .views import ChangePasswordView, PasswordResetConfirmView, PasswordResetRequestView, RegisterView, LoginView, UserView, LogoutView, RefreshTokenView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('refresh-token', RefreshTokenView.as_view()),
    path('change-password', ChangePasswordView.as_view()),
    path('password-reset-request', PasswordResetRequestView.as_view()),
    path('password-reset-confirm', PasswordResetConfirmView.as_view()),
]