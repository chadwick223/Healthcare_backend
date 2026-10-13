from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Patient
from core.api.serializers import (
    LoginSerializer,
    PatientSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data["user"]
            return Response(
                {
                    "message": "Login successful",
                    "access": data["access"],
                    "refresh": data["refresh"],
                    "user": {
                        "id": user.id,
                        "name": user.first_name,
                        "email": user.email,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = Patient.objects.filter(created_by=request.user).order_by('-created_at')
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save(created_by=request.user)
            return Response(
                {
                    "message": "Patient added successfully",
                    "patient": PatientSerializer(patient).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return Patient.objects.filter(id=pk, created_by=user).first()

    def get(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            updated_patient = serializer.save()
            return Response(
                {
                    "message": "Patient updated successfully",
                    "patient": PatientSerializer(updated_patient).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = self.get_object(pk, request.user)
        if patient is None:
            return Response(
                {"error": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        patient.delete()
        return Response(
            {"message": "Patient record deleted successfully."},
            status=status.HTTP_200_OK,
        )


# Backward compatibility alias
PatientCreateView = PatientListCreateView
