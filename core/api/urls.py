from django.urls import path
from core.api.views import (
    DoctorDetailView,
    DoctorListCreateView,
    LoginView,
    PatientDetailView,
    PatientDoctorMappingDetailView,
    PatientDoctorMappingListCreateView,
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

    # Doctor collection endpoints (GET list, POST create)
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors', DoctorListCreateView.as_view(), name='doctor-list-create-noslash'),

    # Doctor item endpoints (GET detail, PUT update, DELETE)
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctors/<int:pk>', DoctorDetailView.as_view(), name='doctor-detail-noslash'),

    # Mapping collection endpoints (GET list, POST assign)
    path('mappings/', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('mappings', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create-noslash'),

    # Mapping item endpoints (GET doctors for patient, DELETE remove mapping)
    path('mappings/<int:pk>/', PatientDoctorMappingDetailView.as_view(), name='mapping-detail'),
    path('mappings/<int:pk>', PatientDoctorMappingDetailView.as_view(), name='mapping-detail-noslash'),
]
