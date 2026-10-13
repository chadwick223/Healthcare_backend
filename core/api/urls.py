from django.urls import path
from core.api.views import (
    LoginView,
    PatientDetailView,
    PatientListCreateView,
    RegisterView,
)

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/register', RegisterView.as_view(), name='auth-register-noslash'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/login', LoginView.as_view(), name='auth-login-noslash'),

    # Patient collection endpoints (GET list, POST create)
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients', PatientListCreateView.as_view(), name='patient-list-create-noslash'),

    # Patient item endpoints (GET detail, PUT update, DELETE)
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/<int:pk>', PatientDetailView.as_view(), name='patient-detail-noslash'),
]
