from django.urls import path
from core.api.views import LoginView, RegisterView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/register', RegisterView.as_view(), name='auth-register-noslash'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/login', LoginView.as_view(), name='auth-login-noslash'),
]
